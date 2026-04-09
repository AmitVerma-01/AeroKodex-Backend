from django.urls import path
from .views import (
    WorkshopCategoryListView,
    WorkshopListView,
    WorkshopDetailView,
    BookingCreateView,
    UserBookingsView,
)

app_name = 'workshops'

urlpatterns = [
    path('categories/', WorkshopCategoryListView.as_view(), name='category-list'),
    path('', WorkshopListView.as_view(), name='workshop-list'),
    path('bookings/', UserBookingsView.as_view(), name='user-bookings'),
    path('<slug:slug>/', WorkshopDetailView.as_view(), name='workshop-detail'),
    path('<slug:slug>/book/', BookingCreateView.as_view(), name='workshop-book'),
]
