from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Avg, Count, F
from django_filters.rest_framework import DjangoFilterBackend

from .models import Transfer, IconsAfterName
from common.models import City, Tag, Country
from .serializers import TransferSerializer, TransferDetailSerializer, TransferCommentsSerializer, \
    IconsAfterNameSerializer
import django_filters
from pagination.pagination import BookingPagination


class TransferFilter(django_filters.FilterSet):
    city = django_filters.ModelChoiceFilter(queryset=City.objects.all())
    departure_date = django_filters.DateFilter()
    return_date = django_filters.DateFilter()

    class Meta:
        model = Transfer
        fields = ['city', 'departure_date', 'return_date']


class TransferViewSet(viewsets.ModelViewSet):
    serializer_class = TransferSerializer
    filterset_class = TransferFilter
    filter_backends = [DjangoFilterBackend]
    pagination_class = BookingPagination

    def get_queryset(self):
        queryset = Transfer.objects.annotate(
            rating=(Avg('comments__rate') * 2),
            rating_quantity=Count('comments'),
            country_name=F('city__country__name'),
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
        instance = Transfer.objects.filter(id=kwargs.get('pk')).annotate(
            rating=Avg('comments__rate'),
            rating_quantity=Count('comments'),
            country_name=F('city__country__name'),
        ).prefetch_related('tags').first()

        serializer = TransferDetailSerializer(instance)
        return Response(serializer.data)

    @action(detail=True, methods=['POST'])
    def add_comment(self, request, pk=None):
        transfer = self.get_object()
        serializer = TransferCommentsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(transfer=transfer, is_approved=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IconsAfterNameViewSet(viewsets.ModelViewSet):
    queryset = IconsAfterName
    serializer_class = IconsAfterNameSerializer
