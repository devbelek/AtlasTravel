from rest_framework import serializers
from .models import Transfer, TransferImage, TransferComments, TransferInquiry, IconsAfterName
from common.serializers import TagSerializer


class TransferImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransferImage
        fields = ['id', 'image']


class TransferCommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransferComments
        fields = '__all__'


class TransferInquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = TransferInquiry
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


class TransferDetailSerializer(serializers.ModelSerializer):
    images = TransferImageSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    comments = serializers.SerializerMethodField(read_only=True)
    similar_transfers = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Transfer
        fields = '__all__'

    def get_comments(self, obj):
        approved_comments = obj.comments.filter(is_approved=True)
        return TransferCommentsSerializer(approved_comments, many=True).data

    def get_similar_transfers(self, obj):
        request = self.context.get('request')
        similar_transfers = obj.find_similar_transfers()
        serializer = TransferSerializer(similar_transfers, many=True, context={'request': request})
        return serializer.data


class IconsAfterNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = IconsAfterName
        fields = '__all__'
