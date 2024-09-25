from rest_framework import serializers
from .models import Transfer, City, Tag, TransferImage, Comments, Inquiry


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class TransferImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransferImage
        fields = ['id', 'image']


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'


class TransferSerializer(serializers.ModelSerializer):
    rating = serializers.FloatField(source='get_final_rating', read_only=True)
    rating_quantity = serializers.IntegerField(source='rating_count', read_only=True)
    image = serializers.SerializerMethodField(read_only=True)
    country_name = serializers.CharField(read_only=True)

    class Meta:
        model = Transfer
        exclude = ('tags', 'description')

    def get_image(self, obj):
        image = obj.images.first()
        if image:
            return TransferImageSerializer(image).data
        return None


class InquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inquiry
        fields = '__all__'


class TransferDetailSerializer(serializers.ModelSerializer):
    images = TransferImageSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    comments = CommentsSerializer(many=True, read_only=True)

    class Meta:
        model = Transfer
        fields = '__all__'
