from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TourViewSet

router = DefaultRouter()
router.register(r'tours', TourViewSet, basename='tours')

urlpatterns = [
    path('', include(router.urls)),
    path('tours/<int:pk>/add_comment/', TourViewSet.as_view({'post': 'add_comment'}), name='tours-add-comment'),
    path('tours/<int:pk>/add_inquiry/', TourViewSet.as_view({'post': 'add_inquiry'}), name='flights-add-inquiry'),
]