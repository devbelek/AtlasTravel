from rest_framework import serializers
from .models import Tour, City, Tag, TourImage, Comments, Inquiry


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class TourImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourImage
        fields = ['id', 'image']


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'


class TourSerializer(serializers.ModelSerializer):
    rating = serializers.FloatField(source='get_final_rating', read_only=True)
    rating_quantity = serializers.IntegerField(source='rating_count', read_only=True)
    image = serializers.SerializerMethodField(read_only=True)
    country_name = serializers.CharField(read_only=True)

    class Meta:
        model = Tour
        exclude = ('tags', 'description')

    def get_image(self, obj):
        image = obj.images.first()
        if image:
            return TourImageSerializer(image).data
        return None


class InquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inquiry
        fields = '__all__'


class TourDetailSerializer(serializers.ModelSerializer):
    images = TourImageSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    comments = CommentsSerializer(many=True, read_only=True)

    class Meta:
        model = Tour
        fields = '__all__'

    def get_comments(self, obj):
        approved_comments = obj.comments.filter(is_approved=True)
        return CommentsSerializer(approved_comments, many=True).data
