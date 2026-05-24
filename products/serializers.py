from rest_framework import serializers
from .models import Category, Product, ProductVariant, ProductImage


class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'product_count']

    def get_product_count(self, obj):
        return obj.products.filter(is_active=True).count()


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'is_feature']


class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ['id', 'variant_name', 'specs', 'datasheet_url', 'price', 'sku', 'stock']


class ProductVariantPublicSerializer(serializers.ModelSerializer):
    """Variant serializer that hides pricing for unauthenticated users."""

    class Meta:
        model = ProductVariant
        fields = ['id', 'variant_name', 'specs', 'datasheet_url', 'sku', 'stock']


class ProductListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    feature_image = serializers.SerializerMethodField()
    variant_count = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description', 'category',
            'feature_image', 'variant_count', 'is_active',
            'meta_title', 'meta_description', 'created_at',
        ]

    def get_feature_image(self, obj):
        featured = obj.images.filter(is_feature=True).first()
        if featured:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(featured.image.url)
            return featured.image.url
        return None

    def get_variant_count(self, obj):
        return obj.variants.count()


class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    variants = serializers.SerializerMethodField()
    related_products = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description', 'technical_specs',
            'category', 'images', 'variants', 'related_products', 'is_active',
            'meta_title', 'meta_description', 'meta_keywords', 'created_at', 'updated_at',
        ]

    def get_related_products(self, obj):
        related = Product.objects.filter(
            category=obj.category, 
            is_active=True
        ).exclude(id=obj.id)[:4]
        return ProductListSerializer(related, many=True, context=self.context).data

    def get_variants(self, obj):
        """Show prices only to authenticated users."""
        request = self.context.get('request')
        if request and request.user and request.user.is_authenticated:
            return ProductVariantSerializer(obj.variants.all(), many=True).data
        return ProductVariantPublicSerializer(obj.variants.all(), many=True).data
