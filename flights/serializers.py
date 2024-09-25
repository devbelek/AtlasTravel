from rest_framework import serializers
from .models import Flight, City, Tag, FlightImage, Comments, Inquiry


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class FlightImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlightImage
        fields = ['id', 'image']


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'


class InquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inquiry
        fields = '__all__'


class FlightSerializer(serializers.ModelSerializer):
    rating = serializers.FloatField(source='get_final_rating', read_only=True)
    rating_quantity = serializers.IntegerField(source='rating_count', read_only=True)
    image = serializers.SerializerMethodField(read_only=True)
    country_name = serializers.CharField(read_only=True)

    class Meta:
        model = Flight
        exclude = ('tags', 'description')

    def get_image(self, obj):
        image = obj.images.first()
        if image:
            return FlightImageSerializer(image).data
        return None


class FlightDetailSerializer(serializers.ModelSerializer):
    images = FlightImageSerializer( )
    tags = TagSerializer(many=True, read_only=True)
    comments = CommentsSerializer(many=True, read_only=True)

    class Meta:
        model = Flight
        fields = '__all__'

    def get_comments(self, obj):
        approved_comments = obj.comments.filter(is_approved=True)
        return CommentsSerializer(approved_comments, many=True).data
