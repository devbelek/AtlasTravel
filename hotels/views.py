from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Avg, Count, F, Q
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from .models import Hotel, IconsAfterName, PopularHotels
from common.models import City
from .serializers import (
    HotelSerializer,
    HotelDetailSerializer,
    HotelCommentsSerializer,
    HotelInquirySerializer,
    IconsAfterNameSerializer
)
import django_filters
from pagination.pagination import BookingPagination


class HotelFilter(django_filters.FilterSet):
    city = django_filters.ModelChoiceFilter(queryset=City.objects.all())
    arrival_date = django_filters.DateFilter()
    nights_min = django_filters.NumberFilter(field_name='nights', lookup_expr='gte')
    nights_max = django_filters.NumberFilter(field_name='nights', lookup_expr='lte')

    class Meta:
        model = Hotel
        fields = ['city', 'arrival_date', 'nights_min', 'nights_max']


class HotelViewSet(viewsets.ModelViewSet):
    serializer_class = HotelSerializer
    filterset_class = HotelFilter
    filter_backends = [DjangoFilterBackend]
    pagination_class = BookingPagination

    def get_queryset(self):
        queryset = Hotel.objects.select_related('city').prefetch_related('tags').annotate(
            rating=Avg('comments__rate') * 2,
            rating_quantity=Count('comments'),
            city_name=F('city__name'),
        )
        return queryset

    @method_decorator(cache_page(60 * 15))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(60 * 15))
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = HotelDetailSerializer(instance, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['POST'])
    def add_comment(self, request, pk=None):
        hotel = self.get_object()
        serializer = HotelCommentsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(hotel=hotel, is_approved=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['POST'])
    def send_inquiry(self, request, pk=None):
        hotel = self.get_object()
        serializer = HotelInquirySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(hotel=hotel)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['GET'])
    @method_decorator(cache_page(60 * 15))
    def similar(self, request, pk=None):
        hotel = self.get_object()
        similar_hotels = hotel.find_similar_hotels()
        serializer = HotelSerializer(similar_hotels, many=True, context={'request': request})
        return Response(serializer.data)

    def perform_create(self, serializer):
        hotel = serializer.save()
        self._update_special_lists(hotel)

    def perform_update(self, serializer):
        hotel = serializer.save()
        self._update_special_lists(hotel)

    def _update_special_lists(self, hotel):
        if hotel.is_popular_hotel:
            PopularHotels.objects.update_or_create(id=hotel.id, defaults={'title': hotel.title, 'city': hotel.city})
        else:
            PopularHotels.objects.filter(id=hotel.id).delete()


class IconsAfterNameViewSet(viewsets.ModelViewSet):
    queryset = IconsAfterName.objects.all()
    serializer_class = IconsAfterNameSerializer
