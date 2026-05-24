from django.contrib import admin
from .models import WorkshopCategory, Workshop, Booking, WorkshopGalleryImage

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
    list_display = ('title', 'category', 'level', 'difficulty', 'date', 'seats_available', 'is_active')
    list_filter = ('category', 'level', 'difficulty', 'is_active')
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
        count = queryset.count()
        self.message_user(request, f"Successfully sent reminder emails to {count} attendees.")
    send_reminder_email.short_description = "Send Email Notification to Attendees"


@admin.register(WorkshopGalleryImage)
class WorkshopGalleryImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'workshop', 'order', 'is_featured', 'created_at')
    list_filter = ('category', 'workshop', 'is_featured')
    search_fields = ('title', 'caption')
    ordering = ('order', '-created_at')

