import asyncio
from .bot import bot_application, send_notification
from django.conf import settings


async def async_send_notification(message):
    await send_notification(bot_application.bot, settings.TELEGRAM_CHAT_ID, message)


def send_consultation_notification(inquiry):
    message = f"Новый запрос на консультацию:\nИмя: {inquiry.name}\nТелефон: {inquiry.phone_number}\nEmail: {inquiry.email}\nСообщение: {inquiry.message}"
    asyncio.run(async_send_notification(message))


def send_review_notification(review):
    message = f"Новый отзыв:\nИмя: {review.full_name}\nОценка: {review.rate}\nКомментарий: {review.text}"
    asyncio.run(async_send_notification(message))