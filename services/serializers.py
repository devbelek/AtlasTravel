from rest_framework import serializers
from .models import VisaService, ServiceImage, ServiceFeature


class ServiceImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceImage
        fields = ['id', 'image', 'order']


class ServiceFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceFeature
        fields = ['id', 'title', 'description', 'order']

    def validate_order(self, value):
        if not isinstance(value, int) or value < 1:
            raise serializers.ValidationError("Порядок должен быть положительным числом")
        return value


class VisaServiceSerializer(serializers.ModelSerializer):
    images = ServiceImageSerializer(many=True, read_only=True)
    features = ServiceFeatureSerializer(many=True, read_only=True)

    class Meta:
        model = VisaService
        fields = ['id', 'title', 'subtitle', 'description', 'images', 'features']
