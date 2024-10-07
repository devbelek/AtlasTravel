from rest_framework import viewsets
from .models import BlogPost, BlogSection
from .serializers import BlogPostSerializer, BlogSectionSerializer


class BlogPostViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer


class BlogSectionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BlogSection.objects.all()
    serializer_class = BlogSectionSerializer