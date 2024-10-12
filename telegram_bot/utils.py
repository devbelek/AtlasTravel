from flights.models import FlightInquiry, FlightComments
from tours.models import TourInquiry, TourComments
from hotels.models import HotelInquiry, HotelComments
from transfer.models import TransferInquiry, TransferComments


def mark_as_processed(obj):
    obj.is_processed = True
    obj.save()


def mark_inquiry_as_processed(inquiry):
    mark_as_processed(inquiry)


def mark_review_as_processed(review):
    mark_as_processed(review)


def get_all_unprocessed_inquiries():
    inquiries = []
    for Model in [FlightInquiry, TourInquiry, HotelInquiry, TransferInquiry]:
        inquiries.extend(Model.objects.filter(is_processed=False))
    return sorted(inquiries, key=lambda x: x.created_at, reverse=True)


def get_all_unprocessed_reviews():
    reviews = []
    for Model in [FlightComments, TourComments, HotelComments, TransferComments]:
        reviews.extend(Model.objects.filter(is_processed=False))
    return sorted(reviews, key=lambda x: x.created_at, reverse=True)