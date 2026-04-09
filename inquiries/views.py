from rest_framework import generics
from rest_framework.permissions import AllowAny

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

    # TODO: Add email notification to admin on successful submission
    # TODO: Add rate limiting via throttling


class QuoteRequestCreateView(generics.CreateAPIView):
    """
    Accept a multi-step quote request.
    No authentication required.
    """
    queryset = QuoteRequest.objects.all()
    serializer_class = QuoteRequestSerializer
    permission_classes = [AllowAny]

    # TODO: Add email confirmation to user on successful submission
    # TODO: Add rate limiting via throttling
