from django.db import models


class Project(models.Model):
    """Completed projects / portfolio items."""

    CATEGORY_CHOICES = [
        ('FABRICATION', 'Fabrication'),
        ('MATERIAL_SUPPLY', 'Material Supply'),
        ('DEVELOPMENT', 'Development'),
        ('TRAINING', 'Training'),
        ('RESEARCH', 'Research'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    client_name = models.CharField(max_length=200, blank=True, default='')
    industry = models.CharField(max_length=100, blank=True, default='')
    description = models.TextField()
    challenges = models.TextField(blank=True, default='', help_text="Challenges faced during the project")
    solutions = models.TextField(blank=True, default='', help_text="Solutions implemented")
    technologies_used = models.JSONField(default=list, help_text="List of technologies used")
    featured_image = models.ImageField(upload_to='projects/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    completed_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # SEO fields
    meta_title = models.CharField(max_length=70, blank=True)
    meta_description = models.TextField(max_length=160, blank=True)

    class Meta:
        ordering = ['-completed_date', '-created_at']
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'

    def __str__(self):
        return self.title


class ProjectImage(models.Model):
    """Additional images/videos for a project."""
    project = models.ForeignKey(Project, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='projects/gallery/')
    caption = models.CharField(max_length=200, blank=True, default='')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Image for {self.project.title}"
