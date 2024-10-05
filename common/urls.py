from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TagViewSet, CountryViewSet, CityViewSet, CommentsViewSet, InquiryViewSet

router = DefaultRouter()
router.register(r'tags', TagViewSet, basename='tags')
router.register(r'country', CountryViewSet, basename='country')
router.register(r'city', CityViewSet, basename='city')
router.register(r'comments', CommentsViewSet, basename='comments')
router.register(r'inquiry', InquiryViewSet, basename='inquiry')


urlpatterns = [
    path('', include(router.urls)),
]