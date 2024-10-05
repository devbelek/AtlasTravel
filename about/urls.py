from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AboutUsViewSet, AboutUsImageViewSet, FAQViewSet, AboutUsInquiryViewSet, AboutUsConsultantViewSet, \
    OurProjectsViewSet

router = DefaultRouter()
router.register(r'about-us', AboutUsViewSet, basename='about')
router.register(r'about-us-images', AboutUsImageViewSet, basename='about-us-images')
router.register(r'faqs', FAQViewSet)
router.register(r'faqs', AboutUsInquiryViewSet)
router.register(r'consultants', AboutUsConsultantViewSet, basename='consultant')
router.register(r'our-projects', OurProjectsViewSet, basename='our-projects')

urlpatterns = [
    path('', include(router.urls)),
]
