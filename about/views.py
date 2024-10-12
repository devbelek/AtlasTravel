from rest_framework import viewsets
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.response import Response

from .models import (AboutUs, AboutUsImage, FAQ, AboutUsInquiry,
                     AboutUsConsultant, OurProjects, PrivacyPolicy,
                     UserAgreement, ReturnPolicy)
from .serializers import (AboutUsSerializer, AboutUsImageSerializer,
                          AboutUsInquirySerializer, AboutUsConsultantSerializer,
                          OurProjectsSerializer, PrivacyPolicySerializer,
                          UserAgreementSerializer, ReturnPolicySerializer,
                          FAQSerializer)


class FAQViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer

    @method_decorator(cache_page(60 * 15))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class AboutUsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AboutUsSerializer

    def get_queryset(self):
        return AboutUs.objects.prefetch_related('aboutusimage_set')[:1]

    @method_decorator(cache_page(60 * 15))
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_queryset().first()
        if instance is None:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class AboutUsInquiryViewSet(viewsets.ModelViewSet):
    queryset = AboutUsInquiry.objects.all()
    serializer_class = AboutUsInquirySerializer


class AboutUsImageViewSet(viewsets.ModelViewSet):
    queryset = AboutUsImage.objects.all().order_by('order')
    serializer_class = AboutUsImageSerializer


class AboutUsConsultantViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AboutUsConsultant.objects.all()
    serializer_class = AboutUsConsultantSerializer

    @method_decorator(cache_page(60 * 15))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class OurProjectsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = OurProjects.objects.prefetch_related('tours').all()
    serializer_class = OurProjectsSerializer

    def get_object(self):
        return self.queryset.first()

    @method_decorator(cache_page(60 * 15))
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class PrivacyPolicyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PrivacyPolicy.objects.all()
    serializer_class = PrivacyPolicySerializer


class UserAgreementViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UserAgreement.objects.all()
    serializer_class = UserAgreementSerializer


class ReturnPolicyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ReturnPolicy.objects.all()
    serializer_class = ReturnPolicySerializer
