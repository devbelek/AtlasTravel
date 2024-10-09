# transfer/views.py

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Avg, Count, F, Q
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from .models import Transfer, IconsAfterName
from common.models import City
from .serializers import (
    TransferSerializer,
    TransferDetailSerializer,
    TransferCommentsSerializer,
    TransferInquirySerializer,
    IconsAfterNameSerializer
)
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
        queryset = Transfer.objects.select_related('city').prefetch_related('tags').annotate(
            rating=Avg('comments__rate') * 2,
            rating_quantity=Count('comments'),
            country_name=F('city__country__name'),
        )
        return queryset

    @method_decorator(cache_page(60 * 15))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(60 * 15))
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = TransferDetailSerializer(instance, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['POST'])
    def add_comment(self, request, pk=None):
        transfer = self.get_object()
        serializer = TransferCommentsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(transfer=transfer, is_approved=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['POST'])
    def add_inquiry(self, request, pk=None):
        transfer = self.get_object()
        serializer = TransferInquirySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(transfer=transfer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['GET'])
    @method_decorator(cache_page(60 * 15))
    def similar(self, request, pk=None):
        transfer = self.get_object()
        similar_transfers = transfer.find_similar_transfers()
        serializer = TransferSerializer(similar_transfers, many=True, context={'request': request})
        return Response(serializer.data)


class IconsAfterNameViewSet(viewsets.ModelViewSet):
    queryset = IconsAfterName.objects.all()
    serializer_class = IconsAfterNameSerializer
