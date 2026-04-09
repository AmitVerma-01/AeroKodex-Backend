from rest_framework import serializers
from .models import Project, ProjectImage


class ProjectImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectImage
        fields = ['id', 'image', 'caption', 'order']


class ProjectListSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source='get_category_display', read_only=True)

    class Meta:
        model = Project
        fields = [
            'id', 'title', 'slug', 'category', 'category_display',
            'client_name', 'industry', 'description', 'featured_image',
            'technologies_used', 'completed_date', 'meta_title', 'meta_description',
        ]


class ProjectDetailSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    images = ProjectImageSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = [
            'id', 'title', 'slug', 'category', 'category_display',
            'client_name', 'industry', 'description', 'challenges',
            'solutions', 'technologies_used', 'featured_image', 'images',
            'completed_date', 'meta_title', 'meta_description',
            'created_at', 'updated_at',
        ]
