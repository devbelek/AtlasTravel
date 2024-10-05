from rest_framework import serializers
from .models import RestIdea, BestChoice, PopularHotel, RentOfCar, RentOfCarImage, RentOfCarDescription, Benefits
from tours.serializers import TourSerializer
from hotels.serializers import HotelSerializer


class RestIdeaSerializer(serializers.ModelSerializer):
    tours = TourSerializer(many=True, read_only=True)

    class Meta:
        model = RestIdea
        fields = ['id', 'tours']


class BestChoiceSerializer(serializers.ModelSerializer):
    tours = TourSerializer(many=True, read_only=True)

    class Meta:
        model = BestChoice
        fields = ['id', 'tours']


class PopularHotelSerializer(serializers.ModelSerializer):
    hotels = HotelSerializer(many=True, read_only=True)

    class Meta:
        model = PopularHotel
        fields = ['id', 'hotels']


class RentOfCarImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RentOfCarImage
        fields = ['id', 'image', 'order']


class RentOfCarDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RentOfCarDescription
        fields = ['id', 'description', 'order']


class RentOfCarSerializer(serializers.ModelSerializer):
    images = RentOfCarImageSerializer(many=True, read_only=True)
    descriptions = RentOfCarDescriptionSerializer(many=True, read_only=True)

    class Meta:
        model = RentOfCar
        fields = ['id', 'title', 'price', 'images', 'descriptions']


class BenefitsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Benefits
        fields = '__all__'