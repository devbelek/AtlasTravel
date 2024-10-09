from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HotelViewSet, IconsAfterNameViewSet

router = DefaultRouter()
router.register(r'hotels', HotelViewSet, basename='hotels')
router.register(r'icons-after-name', IconsAfterNameViewSet, basename='icons-after-name')

urlpatterns = [
    path('', include(router.urls)),
    path('hotels/<int:pk>/add_comment/', HotelViewSet.as_view({'post': 'add_comment'}), name='hotels-add-comment'),
    path('hotels/<int:pk>/send_inquiry/', HotelViewSet.as_view({'post': 'send_inquiry'}), name='hotels-send-inquiry'),
    path('hotels/<int:pk>/similar/', HotelViewSet.as_view({'get': 'similar'}), name='hotels-similar'),
]
