from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BlogPostViewSet, BlogSectionViewSet

router = DefaultRouter()
router.register(r'blog-posts', BlogPostViewSet)
router.register(r'blog-sections', BlogSectionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
