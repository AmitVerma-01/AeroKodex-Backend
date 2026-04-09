from rest_framework import generics, filters, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import WorkshopCategory, Workshop, Booking
from .serializers import (
    WorkshopCategorySerializer,
    WorkshopListSerializer,
    WorkshopDetailSerializer,
    BookingCreateSerializer,
    BookingListSerializer,
)


class WorkshopCategoryListView(generics.ListAPIView):
    """List all workshop categories."""
    queryset = WorkshopCategory.objects.all()
    serializer_class = WorkshopCategorySerializer
    permission_classes = [AllowAny]
    pagination_class = None


class WorkshopListView(generics.ListAPIView):
    """
    List active workshops.
    Supports: ?category=<slug>, ?difficulty=<level>, ?search=<term>
    """
    serializer_class = WorkshopListSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        'category__slug': ['exact'],
        'difficulty': ['exact'],
    }
    search_fields = ['title', 'description']
    ordering_fields = ['date', 'title']
    ordering = ['date']

    def get_queryset(self):
        return Workshop.objects.filter(is_active=True).select_related('category')


class WorkshopDetailView(generics.RetrieveAPIView):
    """Retrieve a single workshop by slug. Price visible only if authenticated."""
    serializer_class = WorkshopDetailSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'

    def get_queryset(self):
        return Workshop.objects.filter(is_active=True).select_related('category')


class BookingCreateView(generics.CreateAPIView):
    """Book a workshop. Requires authentication."""
    serializer_class = BookingCreateSerializer
    permission_classes = [IsAuthenticated]


class UserBookingsView(generics.ListAPIView):
    """List all bookings for the authenticated user."""
    serializer_class = BookingListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).select_related('workshop')
