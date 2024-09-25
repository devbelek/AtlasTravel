from .models import AboutUs, AboutUsImage
from rest_framework import serializers


class AboutUsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutUsImage
        fields = ['id', 'image']


class AboutUsSerializer(serializers.ModelSerializer):
    image = AboutUsImageSerializer(many=True, read_only=True)

    class Meta:
        model = AboutUs
        fields = '__all__'
