from rest_framework import serializers
from .models import Hotel, HotelImage, HotelComments, HotelInquiry, IconsAfterName
from common.serializers import TagSerializer


class HotelImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelImage
        fields = ['id', 'image']


class HotelCommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelComments
        fields = '__all__'


class HotelInquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelInquiry
        fields = '__all__'


class HotelSerializer(serializers.ModelSerializer):
    rating = serializers.FloatField(source='get_final_rating', read_only=True)
    rating_quantity = serializers.IntegerField(source='rating_count', read_only=True)
    image = serializers.SerializerMethodField(read_only=True)
    city_name = serializers.CharField(read_only=True)

    class Meta:
        model = Hotel
        exclude = ('tags', 'description')

    def get_image(self, obj):
        image = obj.images.first()
        if image:
            return HotelImageSerializer(image).data
        return None


class HotelDetailSerializer(serializers.ModelSerializer):
    images = HotelImageSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    comments = HotelCommentsSerializer(many=True, read_only=True)

    class Meta:
        model = Hotel
        fields = '__all__'

    def get_comments(self, obj):
        approved_comments = obj.comments.filter(is_approved=True)
        return HotelCommentsSerializer(approved_comments, many=True).data


class IconsAfterNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = IconsAfterName
        fields = '__all__'