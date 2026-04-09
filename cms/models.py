from django.db import models

class SiteContent(models.Model):
    """For Homepage sections, About, Contact page content"""
    section_key = models.CharField(max_length=100, unique=True, help_text="e.g. 'home_hero', 'about_vision'")
    title = models.CharField(max_length=255, blank=True)
    content = models.TextField(help_text="HTML or Markdown content")
    image = models.ImageField(upload_to='cms/site/', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Section: {self.section_key}"

class Testimonial(models.Model):
    client_name = models.CharField(max_length=200)
    company = models.CharField(max_length=200, blank=True)
    content = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5, help_text="1 to 5")
    image = models.ImageField(upload_to='cms/testimonials/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Testimonial from {self.client_name}"

class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    author = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)
    content = models.TextField(help_text="Rich text content")
    cover_image = models.ImageField(upload_to='cms/blog/', blank=True, null=True)
    is_published = models.BooleanField(default=False)
    published_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # SEO fields
    meta_title = models.CharField(max_length=70, blank=True)
    meta_description = models.TextField(max_length=160, blank=True)

    def __str__(self):
        return self.title
