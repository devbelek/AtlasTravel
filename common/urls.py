from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TagViewSet, CountryViewSet, CityViewSet, CommentsViewSet, InquiryViewSet

router = DefaultRouter()
router.register(r'tags', TagViewSet, basename='tags')
router.register(r'countries', CountryViewSet, basename='countries')
router.register(r'cities', CityViewSet, basename='cities')
router.register(r'comments', CommentsViewSet, basename='comments')
router.register(r'inquiries', InquiryViewSet, basename='inquiries')

urlpatterns = [
    path('', include(router.urls)),
]
