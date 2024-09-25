from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HotelViewSet

router = DefaultRouter()
router.register(r'hotels', HotelViewSet, basename='hotels')

urlpatterns = [
    path('', include(router.urls)),
    path('hotels/<int:pk>/add_comment/', HotelViewSet.as_view({'post': 'add_comment'}), name='hotels-add-comment'),
    path('hotels/<int:pk>/send_inquiry/', HotelViewSet.as_view({'post': 'send_inquiry'}), name='hotels-send-inquiry'),
]
