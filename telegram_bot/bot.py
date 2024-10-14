import asyncio
import json
import logging
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from django.conf import settings
from telegram_bot.utils import (
    get_all_unprocessed_inquiries, get_all_unprocessed_reviews,
    mark_inquiry_as_processed, mark_review_as_processed,
    get_unprocessed_about_us_inquiries, mark_about_us_inquiry_as_processed,
    get_statistics, get_all_admin_chat_ids, add_admin_user, remove_admin_user
)
from asgiref.sync import sync_to_async
import redis

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

redis_client = redis.Redis.from_url(settings.REDIS_URL)
bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Новые запросы", callback_data='new_inquiries')],
        [InlineKeyboardButton("Новые отзывы", callback_data='new_reviews')],
        [InlineKeyboardButton("Запросы 'О нас'", callback_data='about_us_inquiries')],
        [InlineKeyboardButton("Статистика", callback_data='statistics')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Добро пожаловать! Выберите действие:",
        reply_markup=reply_markup
    )


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'new_inquiries':
        await new_inquiries(update, context)
    elif query.data == 'new_reviews':
        await new_reviews(update, context)
    elif query.data == 'about_us_inquiries':
        await about_us_inquiries(update, context)
    elif query.data == 'statistics':
        await show_statistics(update, context)


async def new_inquiries(update: Update, context: ContextTypes.DEFAULT_TYPE):
    inquiries = await sync_to_async(get_all_unprocessed_inquiries)()
    if inquiries:
        for inquiry in inquiries:
            message = f"Новый запрос:\n\nТип: {inquiry._meta.verbose_name}\n"
            message += f"Имя: {inquiry.name}\nТелефон: {inquiry.phone_number}\nEmail: {inquiry.email}\nСообщение: {inquiry.message}\n"

            keyboard = [
                [InlineKeyboardButton("Отметить как обработанный",
                                      callback_data=f'process_inquiry_{inquiry.id}_{inquiry._meta.model_name}')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=message,
                reply_markup=reply_markup
            )
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Новых запросов нет.")


async def new_reviews(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reviews = await sync_to_async(get_all_unprocessed_reviews)()
    if reviews:
        for review in reviews:
            message = f"Новый отзыв:\n\nТип: {review._meta.verbose_name}\n"
            message += f"Имя: {review.full_name}\nОценка: {review.rate}\nКомментарий: {review.text}\n"

            keyboard = [
                [InlineKeyboardButton("Отметить как обработанный",
                                      callback_data=f'process_review_{review.id}_{review._meta.model_name}')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=message,
                reply_markup=reply_markup
            )
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Новых отзывов нет.")


async def about_us_inquiries(update: Update, context: ContextTypes.DEFAULT_TYPE):
    inquiries = await sync_to_async(get_unprocessed_about_us_inquiries)()
    if inquiries:
        for inquiry in inquiries:
            message = f"Новый запрос 'О нас':\n\nТелефон: {inquiry.phone_number}\nДата создания: {inquiry.created_at}\n"

            keyboard = [
                [InlineKeyboardButton("Отметить как обработанный", callback_data=f'process_about_us_{inquiry.id}')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=message,
                reply_markup=reply_markup
            )
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Новых запросов 'О нас' нет.")


async def process_item(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data.split('_')
    action = data[1]
    item_id = int(data[2])
    model_name = data[3] if len(data) > 3 else None

    if action == 'inquiry':
        await sync_to_async(mark_inquiry_as_processed)(item_id, model_name)
        await query.edit_message_text(text="Запрос отмечен как обработанный.")
    elif action == 'review':
        await sync_to_async(mark_review_as_processed)(item_id, model_name)
        await query.edit_message_text(text="Отзыв отмечен как обработанный.")
    elif action == 'about':
        await sync_to_async(mark_about_us_inquiry_as_processed)(item_id)
        await query.edit_message_text(text="Запрос 'О нас' отмечен как обработанный.")


async def show_statistics(update: Update, context: ContextTypes.DEFAULT_TYPE):
    stats = await sync_to_async(get_statistics)()
    message = "Статистика:\n\n"
    for key, value in stats.items():
        message += f"{key}: {value}\n"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)


async def send_notification(message):
    admin_chat_ids = await sync_to_async(get_all_admin_chat_ids)()
    for chat_id in admin_chat_ids:
        try:
            await bot.send_message(chat_id=chat_id, text=message, parse_mode='Markdown')
        except Exception as e:
            logging.error(f"Error sending message to chat_id {chat_id}: {e}")


async def process_notification_queue():
    while True:
        try:
            _, notification = redis_client.brpop('telegram_notifications')
            notification = json.loads(notification)
            await send_notification(notification['content'])
        except Exception as e:
            logging.error(f"Error processing notification: {e}")
        await asyncio.sleep(1)


async def add_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type != 'private':
        await update.message.reply_text("Эта команда доступна только в личных сообщениях.")
        return

    chat_id = update.effective_chat.id
    result = await sync_to_async(add_admin_user)(chat_id)

    if result:
        await update.message.reply_text("Вы успешно добавлены как администратор.")
    else:
        await update.message.reply_text("Вы уже являетесь администратором.")


async def remove_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type != 'private':
        await update.message.reply_text("Эта команда доступна только в личных сообщениях.")
        return

    chat_id = update.effective_chat.id
    result = await sync_to_async(remove_admin_user)(chat_id)

    if result:
        await update.message.reply_text("Вы успешно удалены из списка администраторов.")
    else:
        await update.message.reply_text("Вы не являетесь администратором.")


async def main():
    application = ApplicationBuilder().token(settings.TELEGRAM_BOT_TOKEN).build()

    await application.initialize()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('add_admin', add_admin))
    application.add_handler(CommandHandler('remove_admin', remove_admin))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(CallbackQueryHandler(process_item, pattern='^process_'))

    await asyncio.gather(
        application.start(),
        process_notification_queue()
    )

if __name__ == '__main__':
    asyncio.run(main())