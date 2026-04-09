from rest_framework import serializers
from .models import SiteContent, Testimonial, BlogPost

class SiteContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteContent
        fields = ['section_key', 'title', 'content', 'image', 'is_active']

class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = ['id', 'client_name', 'company', 'content', 'rating', 'image', 'created_at']

class BlogPostListSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
    
    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'slug', 'author_name', 'cover_image', 'published_date']

class BlogPostDetailSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
    
    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'slug', 'author_name', 'content', 'cover_image', 'published_date', 'meta_title', 'meta_description']
