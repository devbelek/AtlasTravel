import json
from django.core.serializers.json import DjangoJSONEncoder
from django.conf import settings
import redis
from django.apps import apps
from django.db.models import Count

redis_client = redis.Redis.from_url(settings.REDIS_URL)


def get_model(app_label, model_name):
    return apps.get_model(app_label, model_name)


def mark_as_processed(obj):
    obj.is_processed = True
    obj.save()


def mark_inquiry_as_processed(item_id, model_name):
    model = get_model_for_inquiry(model_name)
    inquiry = model.objects.get(id=item_id)
    mark_as_processed(inquiry)


def mark_review_as_processed(item_id, model_name):
    model = get_model_for_review(model_name)
    review = model.objects.get(id=item_id)
    mark_as_processed(review)


def mark_about_us_inquiry_as_processed(item_id):
    AboutUsInquiry = get_model('about', 'AboutUsInquiry')
    inquiry = AboutUsInquiry.objects.get(id=item_id)
    mark_as_processed(inquiry)


def get_all_unprocessed_inquiries():
    inquiries = []
    for app, model in [('flights', 'FlightInquiry'), ('tours', 'TourInquiry'),
                       ('hotels', 'HotelInquiry'), ('transfer', 'TransferInquiry')]:
        Model = get_model(app, model)
        inquiries.extend(Model.objects.filter(is_processed=False))
    return inquiries


def get_all_unprocessed_reviews():
    reviews = []
    for app, model in [('flights', 'FlightComments'), ('tours', 'TourComments'),
                       ('hotels', 'HotelComments'), ('transfer', 'TransferComments')]:
        Model = get_model(app, model)
        reviews.extend(Model.objects.filter(is_processed=False))
    return reviews


def get_unprocessed_about_us_inquiries():
    AboutUsInquiry = get_model('about', 'AboutUsInquiry')
    return AboutUsInquiry.objects.filter(is_processed=False)


def enqueue_notification(message):
    redis_client.lpush('telegram_notifications', json.dumps(message, cls=DjangoJSONEncoder))


def send_review_notification(review):
    message = {
        'type': 'review',
        'content': f"*Новый отзыв:*\nТип: {review._meta.verbose_name}\n"
                   f"Имя: {review.full_name}\nОценка: {review.rate}\nКомментарий: {review.text}"
    }
    enqueue_notification(message)


def send_consultation_notification(inquiry):
    message = {
        'type': 'inquiry',
        'content': f"*Новый запрос на консультацию:*\nТип: {inquiry._meta.verbose_name}\n"
                   f"Имя: {inquiry.name}\nТелефон: {inquiry.phone_number}\nEmail: {inquiry.email}\nСообщение: {inquiry.message}"
    }
    enqueue_notification(message)


def send_about_us_notification(inquiry):
    message = {
        'type': 'about_us',
        'content': f"*Новый запрос 'О нас':*\nТелефон: {inquiry.phone_number}\nДата создания: {inquiry.created_at}"
    }
    enqueue_notification(message)


def get_model_for_inquiry(model_name):
    app_models = {
        'flightinquiry': ('flights', 'FlightInquiry'),
        'tourinquiry': ('tours', 'TourInquiry'),
        'hotelinquiry': ('hotels', 'HotelInquiry'),
        'transferinquiry': ('transfer', 'TransferInquiry'),
    }
    app_label, model_name = app_models.get(model_name.lower(), (None, None))
    if app_label and model_name:
        return get_model(app_label, model_name)
    raise ValueError(f"Unknown model: {model_name}")


def get_model_for_review(model_name):
    app_models = {
        'flightcomments': ('flights', 'FlightComments'),
        'tourcomments': ('tours', 'TourComments'),
        'hotelcomments': ('hotels', 'HotelComments'),
        'transfercomments': ('transfer', 'TransferComments'),
    }
    app_label, model_name = app_models.get(model_name.lower(), (None, None))
    if app_label and model_name:
        return get_model(app_label, model_name)
    raise ValueError(f"Unknown model: {model_name}")


def get_statistics():
    stats = {}
    for app, model in [('flights', 'FlightInquiry'), ('tours', 'TourInquiry'),
                       ('hotels', 'HotelInquiry'), ('transfer', 'TransferInquiry')]:
        Model = get_model(app, model)
        stats[f"{model} (Всего/Необработанные)"] = f"{Model.objects.count()}/{Model.objects.filter(is_processed=False).count()}"

    for app, model in [('flights', 'FlightComments'), ('tours', 'TourComments'),
                       ('hotels', 'HotelComments'), ('transfer', 'TransferComments')]:
        Model = get_model(app, model)
        stats[f"{model} (Всего/Необработанные)"] = f"{Model.objects.count()}/{Model.objects.filter(is_processed=False).count()}"

    AboutUsInquiry = get_model('about', 'AboutUsInquiry')
    stats["AboutUsInquiry (Всего/Необработанные)"] = f"{AboutUsInquiry.objects.count()}/{AboutUsInquiry.objects.filter(is_processed=False).count()}"

    return stats


def get_all_admin_chat_ids():
    TelegramUser = get_model('telegram_bot', 'TelegramUser')
    return list(TelegramUser.objects.filter(is_admin=True).values_list('chat_id', flat=True))


def add_admin_user(chat_id):
    TelegramUser = get_model('telegram_bot', 'TelegramUser')
    user, created = TelegramUser.objects.get_or_create(chat_id=chat_id)
    if not user.is_admin:
        user.is_admin = True
        user.save()
    return created


def remove_admin_user(chat_id):
    TelegramUser = get_model('telegram_bot', 'TelegramUser')
    try:
        user = TelegramUser.objects.get(chat_id=chat_id)
        user.is_admin = False
        user.save()
        return True
    except TelegramUser.DoesNotExist:
        return False