from rest_framework import serializers
from .models import Tour, City, Tag, TourImage, TourComments, TourInquiry, IconsAfterName
from common.serializers import CitySerializer, TagSerializer, CountrySerializer


class TourImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourImage
        fields = ['id', 'image']


class TourCommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourComments
        fields = '__all__'


class TourSerializer(serializers.ModelSerializer):
    rating = serializers.FloatField(source='get_final_rating', read_only=True)
    rating_quantity = serializers.IntegerField(source='rating_count', read_only=True)
    image = serializers.SerializerMethodField(read_only=True)
    country_name = serializers.CharField(read_only=True)

    class Meta:
        model = Tour
        exclude = ('tags', 'description', 'is_best_choice', 'is_rest_idea')

    def get_image(self, obj):
        image = obj.images.first()
        if image:
            return TourImageSerializer(image).data
        return None


class TourInquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = TourInquiry
        fields = '__all__'


class TourDetailSerializer(serializers.ModelSerializer):
    images = TourImageSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    comments = TourCommentsSerializer(many=True, read_only=True)

    class Meta:
        model = Tour
        fields = '__all__'

    def get_comments(self, obj):
        approved_comments = obj.comments.filter(is_approved=True)
        return TourCommentsSerializer(approved_comments, many=True).data


class IconsAfterNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = IconsAfterName
        fields = '__all__'