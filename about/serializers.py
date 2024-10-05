from tours.serializers import TourSerializer
from .models import AboutUs, AboutUsImage, FAQ, AboutUsInquiry, AboutUsConsultant, OurProjects
from rest_framework import serializers


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['id', 'question', 'answer', 'order']


class AboutUsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutUsImage
        fields = '__all__'


class AboutUsSerializer(serializers.ModelSerializer):
    image = AboutUsImageSerializer(many=True, read_only=True)

    class Meta:
        model = AboutUs
        fields = '__all__'


class AboutUsInquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutUsInquiry
        fields = '__all__'


class AboutUsConsultantSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutUsConsultant
        fields = ['id', 'name', 'surname', 'phone_number', 'whatsapp', 'telegram', 'instagram', 'is_active']


class OurProjectsSerializer(serializers.ModelSerializer):
    tours = TourSerializer(many=True, read_only=True)

    class Meta:
        model = OurProjects
        fields = ['id', 'title', 'description', 'youtube_video_url', 'tours']