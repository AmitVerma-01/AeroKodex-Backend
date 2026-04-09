from rest_framework import serializers
from .models import ContactSubmission, QuoteRequest


class ContactSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactSubmission
        fields = [
            'id', 'name', 'email', 'phone', 'subject',
            'service_interest', 'message', 'attachment', 'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class QuoteRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuoteRequest
        fields = [
            'id',
            # Step 1
            'service_type', 'product_interest',
            # Step 2
            'specifications', 'quantity', 'material_preferences',
            # Step 3
            'name', 'email', 'phone', 'company', 'timeline', 'budget_range',
            # Step 4
            'attachment_1', 'attachment_2', 'attachment_3',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']
