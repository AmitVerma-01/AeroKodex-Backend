import csv
from django.contrib import admin
from django.http import HttpResponse
from .models import ContactSubmission, QuoteRequest


class ExportCsvMixin:
    """Mixin to add CSV export as an admin action."""

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename={meta.verbose_name_plural}.csv'
        writer = csv.writer(response)
        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])
        return response

    export_as_csv.short_description = "Export selected to CSV"


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(ExportCsvMixin, admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'service_interest', 'status', 'created_at')
    list_filter = ('status', 'service_interest', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('id', 'created_at', 'updated_at')
    list_editable = ('status',)
    date_hierarchy = 'created_at'
    actions = ['export_as_csv', 'mark_responded', 'mark_closed']

    def mark_responded(self, request, queryset):
        queryset.update(status='RESPONDED')
    mark_responded.short_description = "Mark selected as Responded"

    def mark_closed(self, request, queryset):
        queryset.update(status='CLOSED')
    mark_closed.short_description = "Mark selected as Closed"


@admin.register(QuoteRequest)
class QuoteRequestAdmin(ExportCsvMixin, admin.ModelAdmin):
    list_display = ('name', 'email', 'service_type', 'timeline', 'status', 'quoted_amount', 'created_at')
    list_filter = ('status', 'service_type', 'timeline', 'created_at')
    search_fields = ('name', 'email', 'service_type', 'specifications')
    readonly_fields = ('id', 'created_at', 'updated_at')
    list_editable = ('status',)
    date_hierarchy = 'created_at'
    actions = ['export_as_csv', 'mark_reviewed', 'mark_converted']

    fieldsets = (
        ('Service Selection', {
            'fields': ('service_type', 'product_interest'),
        }),
        ('Specifications', {
            'fields': ('specifications', 'quantity', 'material_preferences'),
        }),
        ('Contact & Timeline', {
            'fields': ('name', 'email', 'phone', 'company', 'timeline', 'budget_range'),
        }),
        ('Attachments', {
            'fields': ('attachment_1', 'attachment_2', 'attachment_3'),
        }),
        ('Admin Tracking', {
            'fields': ('status', 'admin_notes', 'quoted_amount', 'id', 'created_at', 'updated_at'),
        }),
    )

    def mark_reviewed(self, request, queryset):
        queryset.update(status='REVIEWED')
    mark_reviewed.short_description = "Mark selected as Reviewed"

    def mark_converted(self, request, queryset):
        queryset.update(status='CONVERTED')
    mark_converted.short_description = "Mark selected as Converted"
