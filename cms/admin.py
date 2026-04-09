from django.contrib import admin
from .models import SiteContent, Testimonial, BlogPost

@admin.register(SiteContent)
class SiteContentAdmin(admin.ModelAdmin):
    list_display = ('section_key', 'title', 'is_active')
    search_fields = ('section_key', 'title', 'content')
    list_filter = ('is_active',)

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'company', 'rating', 'is_active')
    list_filter = ('rating', 'is_active')
    search_fields = ('client_name', 'company', 'content')

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_published', 'published_date')
    list_filter = ('is_published',)
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
