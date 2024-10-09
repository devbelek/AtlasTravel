from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Avg, Count, F
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from .models import Tour, IconsAfterName
from common.models import City
from .serializers import (
    TourSerializer,
    TourDetailSerializer,
    TourCommentsSerializer,
    IconsAfterNameSerializer
)
import django_filters
from pagination.pagination import BookingPagination


class TourFilter(django_filters.FilterSet):
    from_city = django_filters.ModelChoiceFilter(queryset=City.objects.all())
    to_city = django_filters.ModelChoiceFilter(queryset=City.objects.all())
    departure_date = django_filters.DateFilter()
    nights_min = django_filters.NumberFilter(field_name='nights', lookup_expr='gte')
    nights_max = django_filters.NumberFilter(field_name='nights', lookup_expr='lte')

    class Meta:
        model = Tour
        fields = ['from_city', 'to_city', 'departure_date', 'nights_min', 'nights_max']


class TourViewSet(viewsets.ModelViewSet):
    serializer_class = TourSerializer
    filterset_class = TourFilter
    filter_backends = [DjangoFilterBackend]
    pagination_class = BookingPagination

    def get_queryset(self):
        queryset = Tour.objects.select_related('from_city', 'to_city').prefetch_related('tags').annotate(
            rating=Avg('comments__rate') * 2,
            rating_quantity=Count('comments'),
            country_name=F('to_city__country__name'),
        )
        return queryset

    @method_decorator(cache_page(60 * 15))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(60 * 15))
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = TourDetailSerializer(instance, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['POST'])
    def add_comment(self, request, pk=None):
        tour = self.get_object()
        serializer = TourCommentsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(tour=tour, is_approved=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['GET'])
    @method_decorator(cache_page(60 * 15))
    def similar(self, request, pk=None):
        tour = self.get_object()
        similar_tours = tour.find_similar_tours()
        serializer = TourSerializer(similar_tours, many=True, context={'request': request})
        return Response(serializer.data)

    def perform_create(self, serializer):
        tour = serializer.save()
        self._update_special_lists(tour)

    def perform_update(self, serializer):
        tour = serializer.save()
        self._update_special_lists(tour)

    def _update_special_lists(self, tour):
        from main.models import RestIdea, BestChoice

        rest_idea, _ = RestIdea.objects.get_or_create(id=1)
        if tour.is_rest_idea:
            rest_idea.tours.add(tour)
        else:
            rest_idea.tours.remove(tour)

        best_choice, _ = BestChoice.objects.get_or_create(id=1)
        if tour.is_best_choice:
            best_choice.tours.add(tour)
        else:
            best_choice.tours.remove(tour)


class IconsAfterNameViewSet(viewsets.ModelViewSet):
    queryset = IconsAfterName.objects.all()
    serializer_class = IconsAfterNameSerializer
