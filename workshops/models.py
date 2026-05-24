from django.db import models

class WorkshopCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "Workshop Categories"

    def __str__(self):
        return self.name

class Workshop(models.Model):
    DIFFICULTY_CHOICES = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
    ]
    LEVEL_CHOICES = [
        ('junior', 'Junior (Class 4-8)'),
        ('senior', 'Senior (Class 9-12)'),
    ]

    category = models.ForeignKey(WorkshopCategory, related_name='workshops', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='junior')
    description = models.TextField()
    duration = models.CharField(max_length=50, help_text="e.g. 2 Weeks, 3 Days")
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    date = models.DateTimeField()
    location = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    seats_available = models.PositiveIntegerField()
    total_seats = models.PositiveIntegerField()
    image = models.ImageField(upload_to='workshops/')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Booking(models.Model):
    workshop = models.ForeignKey(Workshop, related_name='bookings', on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', related_name='workshop_bookings', on_delete=models.CASCADE)
    booked_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=20, default='Pending')

    def __str__(self):
        return f"{self.user.email} - {self.workshop.title}"


class WorkshopGalleryImage(models.Model):
    title = models.CharField(max_length=200)
    workshop = models.ForeignKey(Workshop, related_name='gallery_images', on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(WorkshopCategory, related_name='gallery_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='workshop_gallery/')
    caption = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Workshop Gallery Image"
        verbose_name_plural = "Workshop Gallery Images"

    def __str__(self):
        return self.title

