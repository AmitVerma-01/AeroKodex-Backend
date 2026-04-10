from rest_framework import serializers
from .models import WorkshopCategory, Workshop, Booking


class WorkshopCategorySerializer(serializers.ModelSerializer):
    workshop_count = serializers.SerializerMethodField()

    class Meta:
        model = WorkshopCategory
        fields = ['id', 'name', 'slug', 'workshop_count']

    def get_workshop_count(self, obj):
        return obj.workshops.filter(is_active=True).count()


class WorkshopListSerializer(serializers.ModelSerializer):
    category = WorkshopCategorySerializer(read_only=True)
    is_fully_booked = serializers.SerializerMethodField()

    class Meta:
        model = Workshop
        fields = [
            'id', 'title', 'slug', 'description', 'category', 'level',
            'duration', 'difficulty', 'date', 'location',
            'seats_available', 'total_seats', 'image',
            'is_active', 'is_fully_booked',
        ]

    def get_is_fully_booked(self, obj):
        return obj.seats_available <= 0


class WorkshopDetailSerializer(serializers.ModelSerializer):
    category = WorkshopCategorySerializer(read_only=True)
    is_fully_booked = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    class Meta:
        model = Workshop
        fields = [
            'id', 'title', 'slug', 'description', 'category', 'level',
            'duration', 'difficulty', 'date', 'location',
            'price', 'seats_available', 'total_seats', 'image',
            'is_active', 'is_fully_booked',
        ]

    def get_is_fully_booked(self, obj):
        return obj.seats_available <= 0

    def get_price(self, obj):
        """Show price only to authenticated users."""
        request = self.context.get('request')
        if request and request.user and request.user.is_authenticated:
            return str(obj.price)
        return None


class BookingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'workshop', 'booked_at', 'payment_status']
        read_only_fields = ['id', 'booked_at', 'payment_status']

    def validate_workshop(self, value):
        if not value.is_active:
            raise serializers.ValidationError("This workshop is no longer active.")
        if value.seats_available <= 0:
            raise serializers.ValidationError("This workshop is fully booked.")
        return value

    def create(self, validated_data):
        user = self.context['request'].user
        workshop = validated_data['workshop']

        # Check for duplicate booking
        if Booking.objects.filter(user=user, workshop=workshop).exists():
            raise serializers.ValidationError("You have already booked this workshop.")

        # Decrement seats
        workshop.seats_available -= 1
        workshop.save(update_fields=['seats_available'])

        return Booking.objects.create(user=user, **validated_data)


class BookingListSerializer(serializers.ModelSerializer):
    workshop_title = serializers.CharField(source='workshop.title', read_only=True)
    workshop_date = serializers.DateTimeField(source='workshop.date', read_only=True)
    workshop_location = serializers.CharField(source='workshop.location', read_only=True)

    class Meta:
        model = Booking
        fields = [
            'id', 'workshop', 'workshop_title', 'workshop_date',
            'workshop_location', 'booked_at', 'payment_status',
        ]
