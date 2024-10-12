import json
from django.core.serializers.json import DjangoJSONEncoder
from django.conf import settings
import redis
from django.apps import apps
from asgiref.sync import async_to_sync

redis_client = redis.Redis.from_url(settings.REDIS_URL)

def get_model(app_label, model_name):
    return apps.get_model(app_label, model_name)

def mark_as_processed(obj):
    obj.is_processed = True
    obj.save()

def mark_inquiry_as_processed(inquiry):
    mark_as_processed(inquiry)

def mark_review_as_processed(review):
    mark_as_processed(review)

def get_all_unprocessed_inquiries():
    inquiries = []
    for app, model in [('flights', 'FlightInquiry'), ('tours', 'TourInquiry'),
                       ('hotels', 'HotelInquiry'), ('transfer', 'TransferInquiry')]:
        Model = get_model(app, model)
        inquiries.extend(Model.objects.filter(is_processed=False))
    return sorted(inquiries, key=lambda x: x.created_at, reverse=True)

def get_all_unprocessed_reviews():
    reviews = []
    for app, model in [('flights', 'FlightComments'), ('tours', 'TourComments'),
                       ('hotels', 'HotelComments'), ('transfer', 'TransferComments')]:
        Model = get_model(app, model)
        reviews.extend(Model.objects.filter(is_processed=False))
    return sorted(reviews, key=lambda x: x.created_at, reverse=True)

def enqueue_notification(message):
    redis_client.lpush('telegram_notifications', json.dumps(message, cls=DjangoJSONEncoder))

def send_review_notification(review):
    message = {
        'type': 'review',
        'content': f"Новый отзыв:\nТип: {review._meta.verbose_name}\n"
                   f"Имя: {review.full_name}\nОценка: {review.rate}\nКомментарий: {review.text}"
    }
    enqueue_notification(message)

def send_consultation_notification(inquiry):
    message = {
        'type': 'inquiry',
        'content': f"Новый запрос на консультацию:\nТип: {inquiry._meta.verbose_name}\n"
                   f"Имя: {inquiry.name}\nТелефон: {inquiry.phone_number}\nEmail: {inquiry.email}\nСообщение: {inquiry.message}"
    }
    enqueue_notification(message)