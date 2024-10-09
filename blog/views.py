from rest_framework import viewsets
from .models import BlogPost, BlogSection
from .serializers import BlogPostSerializer, BlogSectionSerializer
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


class BlogPostViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BlogPost.objects.prefetch_related('sections').all()
    serializer_class = BlogPostSerializer

    @method_decorator(cache_page(60 * 15))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(60 * 15))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class BlogSectionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BlogSection.objects.all()
    serializer_class = BlogSectionSerializer
