import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from django.conf import settings

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Я бот вашего туристического сайта. Я буду отправлять уведомления о новых "
                                        "консультациях и отзывах.")


async def send_notification(bot, chat_id, message):
    await bot.send_message(chat_id=chat_id, text=message)


def setup_bot():
    application = ApplicationBuilder().token(settings.TELEGRAM_BOT_TOKEN).build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    return application


bot_application = setup_bot()