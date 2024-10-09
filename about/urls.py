from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (AboutUsViewSet, AboutUsImageViewSet, FAQViewSet,
                    AboutUsInquiryViewSet, AboutUsConsultantViewSet,
                    OurProjectsViewSet, PrivacyPolicyViewSet,
                    UserAgreementViewSet, ReturnPolicyViewSet)

router = DefaultRouter()
router.register(r'about-us', AboutUsViewSet, basename='about-us')
router.register(r'about-us-images', AboutUsImageViewSet,
                basename='about-us-images')
router.register(r'faqs', FAQViewSet, basename='faqs')
router.register(r'inquiries', AboutUsInquiryViewSet, basename='inquiries')
router.register(r'consultants', AboutUsConsultantViewSet,
                basename='consultants')
router.register(r'our-projects', OurProjectsViewSet, basename='our-projects')
router.register(r'privacy-policy', PrivacyPolicyViewSet,
                basename='privacy-policy')
router.register(r'user-agreement', UserAgreementViewSet,
                basename='user-agreement')
router.register(r'return-policy', ReturnPolicyViewSet,
                basename='return-policy')

urlpatterns = [
    path('', include(router.urls)),
]
