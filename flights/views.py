from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Avg, Count, F, Q
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from .models import Flight
from common.models import City
from .serializers import (
    FlightSerializer,
    FlightDetailSerializer,
    FlightCommentsSerializer,
    FlightInquirySerializer
)
import django_filters
from pagination.pagination import BookingPagination


class FlightFilter(django_filters.FilterSet):
    from_city = django_filters.ModelChoiceFilter(queryset=City.objects.all())
    to_city = django_filters.ModelChoiceFilter(queryset=City.objects.all())
    departure_date = django_filters.DateFilter()
    return_date = django_filters.DateFilter(field_name='return_date')
    class_type = django_filters.CharFilter(field_name='class_type')
    passengers = django_filters.NumberFilter(field_name='passengers', lookup_expr='gte')

    class Meta:
        model = Flight
        fields = ['from_city', 'to_city', 'departure_date', 'return_date', 'class_type', 'passengers']


class FlightViewSet(viewsets.ModelViewSet):
    serializer_class = FlightSerializer
    filterset_class = FlightFilter
    filter_backends = [DjangoFilterBackend]
    pagination_class = BookingPagination

    def get_queryset(self):
        queryset = Flight.objects.select_related('from_city', 'to_city').prefetch_related('tags').annotate(
            rating=Avg('comments__rate') * 2,
            rating_quantity=Count('comments'),
            country_name=F('to_city__country__name'),
        ).order_by('id')
        return queryset

    @method_decorator(cache_page(60 * 15))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(60 * 15))
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = FlightDetailSerializer(instance, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['POST'])
    def add_comment(self, request, pk=None):
        flight = self.get_object()
        serializer = FlightCommentsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(flight=flight, is_approved=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['POST'])
    def add_inquiry(self, request, pk=None):
        flight = self.get_object()
        serializer = FlightInquirySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(flight=flight)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['GET'])
    @method_decorator(cache_page(60 * 15))
    def similar(self, request, pk=None):
        flight = self.get_object()
        similar_flights = flight.find_similar_flights()
        serializer = FlightSerializer(similar_flights, many=True, context={'request': request})
        return Response(serializer.data)