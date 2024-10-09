from rest_framework import viewsets
from .models import City, Tag, Country, Comments, Inquiry
from .serializers import CitySerializer, TagSerializer, CountrySerializer, CommentsSerializer, InquirySerializer
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


class CountryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

    @method_decorator(cache_page(60 * 60))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class CityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = City.objects.select_related('country').all()
    serializer_class = CitySerializer

    @method_decorator(cache_page(60 * 60))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    @method_decorator(cache_page(60 * 60))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.filter(is_approved=True)
    serializer_class = CommentsSerializer


class InquiryViewSet(viewsets.ModelViewSet):
    queryset = Inquiry.objects.all()
    serializer_class = InquirySerializer

