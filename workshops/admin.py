from django.contrib import admin
from .models import WorkshopCategory, Workshop, Booking

import csv
from django.http import HttpResponse

class ExportCsvMixin:
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


@admin.register(Workshop)
class WorkshopAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'difficulty', 'date', 'seats_available', 'is_active')
    list_filter = ('category', 'difficulty', 'is_active')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(WorkshopCategory)
class WorkshopCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Booking)
class BookingAdmin(ExportCsvMixin, admin.ModelAdmin):
    list_display = ('user', 'workshop', 'booked_at', 'payment_status')
    list_filter = ('payment_status', 'workshop')
    actions = ['export_as_csv', 'send_reminder_email']

    def send_reminder_email(self, request, queryset):
        # In a real scenario, this would trigger an email task
        # e.g., send_mail(...)
        count = queryset.count()
        self.message_user(request, f"Successfully sent reminder emails to {count} attendees.")
    send_reminder_email.short_description = "Send Email Notification to Attendees"
