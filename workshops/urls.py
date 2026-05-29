from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    WorkshopCategoryListView,
    WorkshopListView,
    WorkshopDetailView,
    BookingCreateView,
    UserBookingsView,
    WorkshopGalleryImageView,
    StudentBookingViewSet,
)
from .payment_views import CreateRazorpayOrderView, VerifyRazorpayPaymentView

app_name = 'workshops'

router = DefaultRouter()
router.register('school/bookings', StudentBookingViewSet, basename='school-bookings')

urlpatterns = [
    path('categories/', WorkshopCategoryListView.as_view(), name='category-list'),
    path('', WorkshopListView.as_view(), name='workshop-list'),
    path('bookings/', UserBookingsView.as_view(), name='user-bookings'),
    path('gallery/', WorkshopGalleryImageView.as_view(), name='gallery-list'),
    
    # Razorpay Payment integration
    path('school/payment/create/', CreateRazorpayOrderView.as_view(), name='school-payment-create'),
    path('school/payment/verify/', VerifyRazorpayPaymentView.as_view(), name='school-payment-verify'),

    path('<slug:slug>/', WorkshopDetailView.as_view(), name='workshop-detail'),
    path('<slug:slug>/book/', BookingCreateView.as_view(), name='workshop-book'),

    # Include Student Bookings ViewSet Router
    path('', include(router.urls)),
]


