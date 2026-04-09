from django.urls import path
from .views import ContactSubmissionCreateView, QuoteRequestCreateView

app_name = 'inquiries'

urlpatterns = [
    path('contact/', ContactSubmissionCreateView.as_view(), name='contact-create'),
    path('quote/', QuoteRequestCreateView.as_view(), name='quote-create'),
]
