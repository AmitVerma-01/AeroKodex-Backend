import uuid
from django.db import models


class ContactSubmission(models.Model):
    """Stores contact form submissions from the website."""

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('RESPONDED', 'Responded'),
        ('CLOSED', 'Closed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, default='')
    subject = models.CharField(max_length=200, blank=True, default='General Inquiry')
    service_interest = models.CharField(max_length=100, blank=True, default='')
    message = models.TextField()
    attachment = models.FileField(upload_to='contact_attachments/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    admin_notes = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Submission'
        verbose_name_plural = 'Contact Submissions'

    def __str__(self):
        return f"{self.name} — {self.subject} ({self.get_status_display()})"


class QuoteRequest(models.Model):
    """Multi-step quote request form data."""

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('REVIEWED', 'Reviewed'),
        ('QUOTED', 'Quoted'),
        ('CONVERTED', 'Converted'),
        ('REJECTED', 'Rejected'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Step 1: Service/product selection
    service_type = models.CharField(
        max_length=100,
        help_text="e.g. Composite Materials, CNC Fabrication, Workshop Training",
    )
    product_interest = models.CharField(max_length=200, blank=True, default='')

    # Step 2: Specifications & requirements
    specifications = models.TextField(help_text="Detailed technical requirements")
    quantity = models.CharField(max_length=50, blank=True, default='')
    material_preferences = models.CharField(max_length=200, blank=True, default='')

    # Step 3: Contact details & timeline
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, default='')
    company = models.CharField(max_length=200, blank=True, default='')
    timeline = models.CharField(
        max_length=50, blank=True, default='',
        help_text="e.g. Urgent, 1-2 Weeks, 1 Month",
    )
    budget_range = models.CharField(max_length=50, blank=True, default='')

    # Step 4: File uploads
    attachment_1 = models.FileField(upload_to='quote_attachments/', blank=True, null=True)
    attachment_2 = models.FileField(upload_to='quote_attachments/', blank=True, null=True)
    attachment_3 = models.FileField(upload_to='quote_attachments/', blank=True, null=True)

    # Admin tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    admin_notes = models.TextField(blank=True, default='')
    quoted_amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Quote Request'
        verbose_name_plural = 'Quote Requests'

    def __str__(self):
        return f"{self.name} — {self.service_type} ({self.get_status_display()})"
