from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    OTPVerifySerializer,
    ResendOTPSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
    UserSerializer,
)


class RegisterView(generics.CreateAPIView):
    """Register a new user. Sends an OTP for email verification."""
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "message": "Registration successful. Please verify your email with the OTP sent.",
                "email": user.email,
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    """Authenticate user and return JWT tokens."""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = data['user']
        return Response(
            {
                "message": "Login successful.",
                "tokens": data['tokens'],
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "username": user.username,
                    "role": user.role,
                },
            },
            status=status.HTTP_200_OK,
        )


class OTPVerifyView(APIView):
    """Verify a user's email using the OTP."""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Email verified successfully. You can now log in."},
            status=status.HTTP_200_OK,
        )


class ResendOTPView(APIView):
    """Resend a verification OTP to the user's email."""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ResendOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "A new OTP has been sent to your email."},
            status=status.HTTP_200_OK,
        )


class PasswordResetRequestView(APIView):
    """Request a password reset OTP."""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Password reset OTP sent to your email."},
            status=status.HTTP_200_OK,
        )


class PasswordResetConfirmView(APIView):
    """Confirm password reset using OTP and set new password."""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Password reset successfully."},
            status=status.HTTP_200_OK,
        )


class ProfileView(generics.RetrieveUpdateAPIView):
    """Get or update the authenticated user's profile."""
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class DashboardView(APIView):
    """
    Returns a summary for the authenticated user's dashboard:
    - Profile info
    - Quote history count
    - Workshop bookings count
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        from workshops.models import Booking
        from inquiries.models import QuoteRequest
        from .models import Wishlist, UserDocument

        bookings_count = Booking.objects.filter(user=user).count()
        quotes_count = QuoteRequest.objects.filter(email=user.email).count()
        wishlist_count = Wishlist.objects.filter(user=user).count()
        documents = UserDocument.objects.filter(user=user).values('id', 'title', 'document_type', 'uploaded_at')

        return Response({
            "user": UserSerializer(user).data,
            "stats": {
                "workshop_bookings": bookings_count,
                "quote_requests": quotes_count,
                "saved_products_wishlist": wishlist_count,
            },
            "documents": list(documents)
        })


from rest_framework import viewsets
from .models import Student
from .serializers import StudentSerializer

class StudentViewSet(viewsets.ModelViewSet):
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role != 'SCHOOL':
            return Student.objects.none()
        return Student.objects.filter(school=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(school=self.request.user)

