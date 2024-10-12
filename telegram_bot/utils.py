from .bot import bot_application, send_notification
from django.conf import settings


def send_consultation_notification(inquiry):
    message = f"Новый запрос на консультацию:\nИмя: {inquiry.name}\nТелефон: {inquiry.phone_number}\nEmail: {inquiry.email}\nСообщение: {inquiry.message}"
    bot_application.bot.create_task(send_notification(bot_application.bot, settings.TELEGRAM_CHAT_ID, message))


def send_review_notification(review):
    message = f"Новый отзыв:\nИмя: {review.full_name}\nОценка: {review.rate}\nКомментарий: {review.text}"
    bot_application.bot.create_task(send_notification(bot_application.bot, settings.TELEGRAM_CHAT_ID, message))