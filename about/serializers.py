from rest_framework import serializers
from tours.serializers import TourSerializer
from .models import (AboutUs, AboutUsImage, FAQ, AboutUsInquiry,
                     AboutUsConsultant, OurProjects, PrivacyPolicy,
                     UserAgreement, ReturnPolicy)

class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['id', 'question', 'answer']

class AboutUsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutUsImage
        fields = '__all__'

class AboutUsSerializer(serializers.ModelSerializer):
    images = AboutUsImageSerializer(many=True, read_only=True,
                                    source='aboutusimage_set')

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
        fields = ['id', 'name', 'surname', 'phone_number', 'whatsapp',
                  'telegram', 'instagram', 'is_active']

class OurProjectsSerializer(serializers.ModelSerializer):
    tours = TourSerializer(many=True, read_only=True)

    class Meta:
        model = OurProjects
        fields = ['id', 'title', 'description', 'youtube_video_url', 'tours']

class PrivacyPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivacyPolicy
        fields = '__all__'

class UserAgreementSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAgreement
        fields = '__all__'

class ReturnPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = ReturnPolicy
        fields = '__all__'
