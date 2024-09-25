from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AboutUsViewSet

router = DefaultRouter()
router.register(r'about', AboutUsViewSet, basename='about')

urlpatterns = [
    path('', include(router.urls)),
]
