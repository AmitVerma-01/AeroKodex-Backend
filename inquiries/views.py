from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.throttling import AnonRateThrottle
from django.core.mail import send_mail
from django.conf import settings

from .models import ContactSubmission, QuoteRequest
from .serializers import ContactSubmissionSerializer, QuoteRequestSerializer


class ContactSubmissionCreateView(generics.CreateAPIView):
    """
    Accept a contact form submission.
    No authentication required.
    """
    queryset = ContactSubmission.objects.all()
    serializer_class = ContactSubmissionSerializer
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]

    def perform_create(self, serializer):
        instance = serializer.save()
        # Send email notification to admin
        send_mail(
            subject=f"New Contact Submission: {instance.subject}",
            message=f"Name: {instance.name}\nEmail: {instance.email}\nPhone: {instance.phone}\nService: {instance.service_interest}\n\nMessage:\n{instance.message}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.DEFAULT_FROM_EMAIL],  # Assuming admin is testing with this
            fail_silently=True,
        )


class QuoteRequestCreateView(generics.CreateAPIView):
    """
    Accept a multi-step quote request.
    No authentication required.
    """
    queryset = QuoteRequest.objects.all()
    serializer_class = QuoteRequestSerializer
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]

    def perform_create(self, serializer):
        instance = serializer.save()
        # Send email confirmation to user
        send_mail(
            subject=f"Quote Request Received: {instance.service_type}",
            message=f"Hi {instance.name},\n\nWe have received your quote request for {instance.service_type}. Our team will review your specifications and get back to you shortly.\n\nThank you,\nAeroKodex Team",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.email],
            fail_silently=True,
        )
        
        # Notify admin
        send_mail(
            subject=f"New Quote Request from {instance.name}",
            message=f"New quote request for {instance.service_type} from {instance.email}. Check admin dashboard for details.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.DEFAULT_FROM_EMAIL],
            fail_silently=True,
        )
