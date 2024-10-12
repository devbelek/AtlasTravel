import asyncio
import json
import logging
import redis
from telegram import Bot
from telegram.ext import ApplicationBuilder, CommandHandler
from django.conf import settings
from telegram_bot.utils import get_all_unprocessed_inquiries, get_all_unprocessed_reviews, mark_inquiry_as_processed, \
    mark_review_as_processed

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

redis_client = redis.Redis.from_url(settings.REDIS_URL)
bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)

async def start(update, context):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Добро пожаловать! Я бот вашего туристического сайта. Используйте следующие команды:\n"
             "/new_inquiries - Показать новые запросы\n"
             "/new_reviews - Показать новые отзывы"
    )

async def new_inquiries(update, context):
    inquiries = get_all_unprocessed_inquiries()
    if inquiries:
        message = "Новые запросы:\n\n"
        for inquiry in inquiries:
            message += f"Тип: {inquiry._meta.verbose_name}\n"
            message += f"Имя: {inquiry.name}\nТелефон: {inquiry.phone_number}\nEmail: {inquiry.email}\nСообщение: {inquiry.message}\n\n"
            mark_inquiry_as_processed(inquiry)
    else:
        message = "Новых запросов нет."

    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)

async def new_reviews(update, context):
    reviews = get_all_unprocessed_reviews()
    if reviews:
        message = "Новые отзывы:\n\n"
        for review in reviews:
            message += f"Тип: {review._meta.verbose_name}\n"
            message += f"Имя: {review.full_name}\nОценка: {review.rate}\nКомментарий: {review.text}\n\n"
            mark_review_as_processed(review)
    else:
        message = "Новых отзывов нет."

    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)

async def send_notification(message):
    admin_chat_id = settings.TELEGRAM_ADMIN_CHAT_ID
    await bot.send_message(chat_id=admin_chat_id, text=message)

async def process_notification_queue():
    while True:
        try:
            _, notification = redis_client.brpop('telegram_notifications')
            notification = json.loads(notification)
            await send_notification(notification['content'])
        except Exception as e:
            logging.error(f"Error processing notification: {e}")
        await asyncio.sleep(1)

async def main():
    application = ApplicationBuilder().token(settings.TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('new_inquiries', new_inquiries))
    application.add_handler(CommandHandler('new_reviews', new_reviews))

    # Запуск цикла событий
    await asyncio.gather(
        application.start(),
        process_notification_queue(),
    )

if __name__ == '__main__':
    asyncio.run(main())