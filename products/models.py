from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    technical_specs = models.JSONField(default=dict, help_text="Store technical specs as key-value pairs")
    views_count = models.PositiveIntegerField(default=0, help_text="Tracks popular products")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # SEO fields
    meta_title = models.CharField(max_length=70, blank=True)
    meta_description = models.TextField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True, help_text="Comma-separated keywords")

    def __str__(self):
        return self.name

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE)
    variant_name = models.CharField(max_length=100, help_text="e.g. BhorForce® PC100")
    specs = models.JSONField(default=dict, help_text="Per-variant specs e.g. {gsm: 100, width_mm: 1000, thickness_mm: 0.13, weave: 'Plain'}")
    datasheet_url = models.URLField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    sku = models.CharField(max_length=50, unique=True, blank=True, null=True)
    stock = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.product.name} - {self.variant_name}"

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')
    is_feature = models.BooleanField(default=False)

    def __str__(self):
        return f"Image for {self.product.name}"
