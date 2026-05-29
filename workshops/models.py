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


class StudentBooking(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('Failed', 'Failed'),
    ]
    school = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='student_bookings', limit_choices_to={'role': 'SCHOOL'})
    student = models.ForeignKey('users.Student', on_delete=models.CASCADE, related_name='bookings')
    workshop = models.ForeignKey('workshops.Workshop', on_delete=models.CASCADE, related_name='student_bookings')
    booked_at = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=4000.00)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='Pending')
    
    # Razorpay details
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        unique_together = ('student', 'workshop')
        ordering = ['-booked_at']

    def __str__(self):
        return f"{self.student.name} - {self.workshop.title} ({self.payment_status})"


