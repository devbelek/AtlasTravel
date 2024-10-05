from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Avg, Count, F
from django_filters.rest_framework import DjangoFilterBackend
from .models import Hotel, HotelInquiry, PopularHotels, IconsAfterName
from common.models import City
from .serializers import HotelSerializer, HotelDetailSerializer, HotelCommentsSerializer, HotelInquirySerializer, \
    IconsAfterNameSerializer
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
        queryset = Hotel.objects.annotate(
            rating=(Avg('comments__rate') * 2),
            rating_quantity=Count('comments'),
            city_name=F('city__name'),
        )
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = Hotel.objects.filter(id=kwargs.get('pk')).annotate(
            rating=(Avg('comments__rate') * 2),
            rating_quantity=Count('comments'),
            city_name=F('city__name'),
        ).prefetch_related('tags').first()

        serializer = HotelDetailSerializer(instance)
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
    queryset = IconsAfterName
    serializer_class = IconsAfterNameSerializer
