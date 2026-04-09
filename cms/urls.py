from django.urls import path
from .views import SiteContentListView, TestimonialListView, BlogPostListView, BlogPostDetailView

app_name = 'cms'

urlpatterns = [
    path('content/', SiteContentListView.as_view(), name='content-list'),
    path('testimonials/', TestimonialListView.as_view(), name='testimonial-list'),
    path('blog/', BlogPostListView.as_view(), name='blog-list'),
    path('blog/<slug:slug>/', BlogPostDetailView.as_view(), name='blog-detail'),
]
