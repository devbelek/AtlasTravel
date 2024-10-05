from rest_framework import serializers
from .models import Flight, FlightImage, FlightComments, FlightInquiry, IconsAfterName
from common.serializers import TagSerializer


class FlightImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlightImage
        fields = ['id', 'image']


class FlightCommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlightComments
        fields = '__all__'


class FlightInquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = FlightInquiry
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
    comments = FlightCommentsSerializer(many=True, read_only=True)

    class Meta:
        model = Flight
        fields = '__all__'

    def get_comments(self, obj):
        approved_comments = obj.comments.filter(is_approved=True)
        return FlightCommentsSerializer(approved_comments, many=True).data


class IconsAfterNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = IconsAfterName
        fields = '__all__'