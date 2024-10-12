from django.apps import apps


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


def send_review_notification(review):
    # Реализация отправки уведомления о новом отзыве
    pass


def send_consultation_notification(inquiry):
    # Реализация отправки уведомления о новом запросе на консультацию
    pass