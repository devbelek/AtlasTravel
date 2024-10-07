from rest_framework import serializers
from .models import BlogPost, BlogSection


class BlogSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogSection
        fields = '__all__'


class BlogPostSerializer(serializers.ModelSerializer):
    sections = BlogSectionSerializer(many=True, read_only=True)

    class Meta:
        model = BlogPost
        fields = '__all__'