from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import SiteContent, Testimonial, BlogPost
from .serializers import SiteContentSerializer, TestimonialSerializer, BlogPostListSerializer, BlogPostDetailSerializer

class SiteContentListView(generics.ListAPIView):
    queryset = SiteContent.objects.filter(is_active=True)
    serializer_class = SiteContentSerializer
    permission_classes = [AllowAny]
    pagination_class = None

class TestimonialListView(generics.ListAPIView):
    queryset = Testimonial.objects.filter(is_active=True).order_by('-created_at')
    serializer_class = TestimonialSerializer
    permission_classes = [AllowAny]

class BlogPostListView(generics.ListAPIView):
    queryset = BlogPost.objects.filter(is_published=True).order_by('-published_date')
    serializer_class = BlogPostListSerializer
    permission_classes = [AllowAny]

class BlogPostDetailView(generics.RetrieveAPIView):
    queryset = BlogPost.objects.filter(is_published=True)
    serializer_class = BlogPostDetailSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'
