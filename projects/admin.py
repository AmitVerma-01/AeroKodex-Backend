from django.contrib import admin
from .models import Project, ProjectImage


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'client_name', 'industry', 'is_active', 'completed_date')
    list_filter = ('category', 'is_active', 'industry')
    search_fields = ('title', 'description', 'client_name')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProjectImageInline]

    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'category', 'featured_image', 'is_active'),
        }),
        ('Project Details', {
            'fields': ('client_name', 'industry', 'description', 'challenges', 'solutions', 'technologies_used', 'completed_date'),
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',),
        }),
    )
