from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter

from .views import (
    RegisterView,
    LoginView,
    OTPVerifyView,
    ResendOTPView,
    PasswordResetRequestView,
    PasswordResetConfirmView,
    ProfileView,
    DashboardView,
    StudentViewSet,
)

app_name = 'users'

router = DefaultRouter()
router.register('school/students', StudentViewSet, basename='school-students')

urlpatterns = [
    # Auth
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('verify-otp/', OTPVerifyView.as_view(), name='verify-otp'),
    path('resend-otp/', ResendOTPView.as_view(), name='resend-otp'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset'),
    path('password-reset/confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),

    # Profile & Dashboard
    path('profile/', ProfileView.as_view(), name='profile'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),

    # School Router URLs
    path('', include(router.urls)),
]

