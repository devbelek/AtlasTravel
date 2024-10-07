from django.core.exceptions import ValidationError

from .models import AboutUs, AboutUsImage, AboutUsInquiry, AboutUsConsultant, OurProjects, UserAgreement, PrivacyPolicy, \
    ReturnPolicy
from .serializers import AboutUsSerializer, AboutUsImageSerializer, AboutUsInquirySerializer, \
    AboutUsConsultantSerializer, OurProjectsSerializer, UserAgreementSerializer, PrivacyPolicySerializer, \
    ReturnPolicySerializer
from rest_framework import viewsets, generics
from .models import FAQ
from .serializers import FAQSerializer


class FAQViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer


class AboutUsViewSet(viewsets.ModelViewSet):
    queryset = AboutUs.objects.all()
    serializer_class = AboutUsSerializer


class AboutUsInquiryViewSet(viewsets.ModelViewSet):
    queryset = AboutUsInquiry.objects.all()
    serializer_class = AboutUsInquirySerializer


class AboutUsImageViewSet(viewsets.ModelViewSet):
    queryset = AboutUsImage.objects.all().order_by('order')
    serializer_class = AboutUsImageSerializer


class AboutUsConsultantViewSet(viewsets.ModelViewSet):
    queryset = AboutUsConsultant.objects.all()
    serializer_class = AboutUsConsultantSerializer


class OurProjectsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = OurProjects.objects.prefetch_related('tours').all()
    serializer_class = OurProjectsSerializer

    def get_object(self):
        return self.queryset.first()


class PrivacyPolicyViewSet(viewsets.ModelViewSet):
    queryset = PrivacyPolicy.objects.all()
    serializer_class = PrivacyPolicySerializer


class UserAgreementViewSet(viewsets.ModelViewSet):
    queryset = UserAgreement.objects.all()
    serializer_class = UserAgreementSerializer


class ReturnPolicyViewSet(viewsets.ModelViewSet):
    queryset = ReturnPolicy.objects.all()
    serializer_class = ReturnPolicySerializer
