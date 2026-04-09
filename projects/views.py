from rest_framework import generics, filters
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend

from .models import Project
from .serializers import ProjectListSerializer, ProjectDetailSerializer


class ProjectListView(generics.ListAPIView):
    """
    List active projects / portfolio items.
    Supports: ?category=<type>, ?industry=<name>, ?search=<term>
    """
    serializer_class = ProjectListSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        'category': ['exact'],
        'industry': ['exact'],
    }
    search_fields = ['title', 'description', 'client_name', 'industry']
    ordering_fields = ['completed_date', 'title']
    ordering = ['-completed_date']

    def get_queryset(self):
        return Project.objects.filter(is_active=True).prefetch_related('images')


class ProjectDetailView(generics.RetrieveAPIView):
    """Retrieve a single project by slug."""
    serializer_class = ProjectDetailSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'

    def get_queryset(self):
        return Project.objects.filter(is_active=True).prefetch_related('images')
