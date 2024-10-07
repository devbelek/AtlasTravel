from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from .models import VisaService, ServiceImage, ServiceFeature
from .serializers import VisaServiceSerializer, ServiceImageSerializer, ServiceFeatureSerializer


class VisaServiceViewSet(viewsets.ModelViewSet):
    queryset = VisaService.objects.all()
    serializer_class = VisaServiceSerializer

    @action(detail=True, methods=['post'])
    @transaction.atomic
    def update_images_order(self, request, pk=None):
        service = self.get_object()
        images_order = request.data.get('images_order', [])

        for order_data in images_order:
            image_id = order_data.get('id')
            new_order = order_data.get('order')
            ServiceImage.objects.filter(id=image_id, service=service).update(order=new_order)

        return Response({'status': 'orders updated'})

    @action(detail=True, methods=['post'])
    @transaction.atomic
    def update_features_order(self, request, pk=None):
        service = self.get_object()
        features_order = request.data.get('features_order', [])

        for order_data in features_order:
            feature_id = order_data.get('id')
            new_order = order_data.get('order')
            ServiceFeature.objects.filter(id=feature_id, service=service).update(order=new_order)

        return Response({'status': 'orders updated'})

