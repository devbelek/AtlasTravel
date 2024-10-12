import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from django.conf import settings
from flights.models import FlightInquiry, FlightComments
from tours.models import TourInquiry, TourComments
from hotels.models import HotelInquiry, HotelComments
from transfer.models import TransferInquiry, TransferComments

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Добро пожаловать! Я бот вашего туристического сайта. Используйте следующие команды:\n"
             "/new_inquiries - Показать новые запросы\n"
             "/new_reviews - Показать новые отзывы\n"
             "Добавьте _flights, _tours, _hotels или _transfer к команде для конкретного раздела."
    )


async def new_inquiries(update: Update, context: ContextTypes.DEFAULT_TYPE):
    inquiry_types = {
        'flights': (FlightInquiry, 'авиаперелет'),
        'tours': (TourInquiry, 'тур'),
        'hotels': (HotelInquiry, 'отель'),
        'transfer': (TransferInquiry, 'трансфер')
    }

    command = update.message.text.split('_')
    if len(command) > 1 and command[1] in inquiry_types:
        InquiryModel, inquiry_type = inquiry_types[command[1]]
        inquiries = InquiryModel.objects.filter(is_processed=False).order_by('-created_at')[:5]
        type_str = f" на {inquiry_type}"
    else:
        inquiries = []
        for InquiryModel, _ in inquiry_types.values():
            inquiries.extend(InquiryModel.objects.filter(is_processed=False).order_by('-created_at')[:5])
        inquiries.sort(key=lambda x: x.created_at, reverse=True)
        inquiries = inquiries[:5]
        type_str = ""

    if inquiries:
        message = f"Новые запросы{type_str}:\n\n"
        for inquiry in inquiries:
            message += f"Тип: {inquiry._meta.verbose_name}\n"
            message += f"Имя: {inquiry.name}\nТелефон: {inquiry.phone_number}\nEmail: {inquiry.email}\nСообщение: {inquiry.message}\n\n"
    else:
        message = f"Новых запросов{type_str} нет."

    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)


async def new_reviews(update: Update, context: ContextTypes.DEFAULT_TYPE):
    review_types = {
        'flights': (FlightComments, 'авиаперелет'),
        'tours': (TourComments, 'тур'),
        'hotels': (HotelComments, 'отель'),
        'transfer': (TransferComments, 'трансфер')
    }

    command = update.message.text.split('_')
    if len(command) > 1 and command[1] in review_types:
        ReviewModel, review_type = review_types[command[1]]
        reviews = ReviewModel.objects.filter(is_processed=False).order_by('-created_at')[:5]
        type_str = f" на {review_type}"
    else:
        reviews = []
        for ReviewModel, _ in review_types.values():
            reviews.extend(ReviewModel.objects.filter(is_processed=False).order_by('-created_at')[:5])
        reviews.sort(key=lambda x: x.created_at, reverse=True)
        reviews = reviews[:5]
        type_str = ""

    if reviews:
        message = f"Новые отзывы{type_str}:\n\n"
        for review in reviews:
            message += f"Тип: {review._meta.verbose_name}\n"
            message += f"Имя: {review.full_name}\nОценка: {review.rate}\nКомментарий: {review.text}\n\n"
    else:
        message = f"Новых отзывов{type_str} нет."

    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)


def setup_bot():
    application = ApplicationBuilder().token(settings.TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('new_inquiries', new_inquiries))
    application.add_handler(CommandHandler('new_reviews', new_reviews))

    # Добавляем обработчики для конкретных типов
    for command in ['new_inquiries_flights', 'new_inquiries_tours', 'new_inquiries_hotels', 'new_inquiries_transfer']:
        application.add_handler(CommandHandler(command, new_inquiries))
    for command in ['new_reviews_flights', 'new_reviews_tours', 'new_reviews_hotels', 'new_reviews_transfer']:
        application.add_handler(CommandHandler(command, new_reviews))

    return application


bot_application = setup_bot()