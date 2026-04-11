import os
import django
from django.utils import timezone
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from workshops.models import WorkshopCategory, Workshop
from products.models import Category, Product, ProductVariant
from projects.models import Project

def seed_data():
    print("Seeding database...")
    
    # 1. Clear existing data
    WorkshopCategory.objects.all().delete()
    Workshop.objects.all().delete()
    Category.objects.all().delete()
    Product.objects.all().delete()
    Project.objects.all().delete()

    print("Existing data cleared.")

    # 2. Seed Workshop Categories
    cat1 = WorkshopCategory.objects.create(name="Aeromodelling", slug="aeromodelling")
    cat2 = WorkshopCategory.objects.create(name="Robotics", slug="robotics")

    # 3. Seed Workshops
    Workshop.objects.create(
        category=cat1,
        title="Intro to Aeromodelling (Junior)",
        slug="intro-to-aeromodelling-junior",
        level='junior',
        description="A foundational workshop on building your first RC plane. Perfect for complete beginners.",
        duration="1 Week",
        difficulty="Beginner",
        date=timezone.now() + timedelta(days=7),
        location="AeroKodex Labs, Kushinagar",
        price=1500.00,
        total_seats=20,
        seats_available=15,
        is_active=True
    )

    Workshop.objects.create(
        category=cat1,
        title="Advanced RC Plane Building",
        slug="advanced-rc-plane-building",
        level='senior',
        description="Learn aerodynamics, thrust vectoring, and advanced RC plane building techniques.",
        duration="3 Weeks",
        difficulty="Advanced",
        date=timezone.now() + timedelta(days=14),
        location="AeroKodex Labs, Kushinagar",
        price=4500.00,
        total_seats=10,
        seats_available=2,
        is_active=True
    )

    Workshop.objects.create(
        category=cat2,
        title="Robotics for Kids",
        slug="robotics-for-kids",
        level='junior',
        description="Learn to build line-following robots and basic automation.",
        duration="2 Weeks",
        difficulty="Beginner",
        date=timezone.now() + timedelta(days=5),
        location="AeroKodex Labs, Mumbai",
        price=2000.00,
        total_seats=25,
        seats_available=20,
        is_active=True
    )

    print("Workshops seeded.")

    # 4. Seed Product Categories
    p_cat1 = Category.objects.create(name="Electronics", slug="electronics")
    p_cat2 = Category.objects.create(name="Airframes", slug="airframes")

    # 5. Seed Products
    prod1 = Product.objects.create(
        category=p_cat1,
        name="Brushless DC Motor 1000KV",
        slug="brushless-dc-motor-1000kv",
        description="High-performance brushless motor suitable for medium-sized RC planes and quadcopters.",
        technical_specs={"Voltage": "11.1V", "Max Current": "20A", "Thrust": "850g"},
        is_active=True
    )

    ProductVariant.objects.create(
        product=prod1,
        variant_name="Default",
        price=850.00,
        sku="BLDC-1000KV",
        stock=50
    )

    prod2 = Product.objects.create(
        category=p_cat2,
        name="Balsa Wood Sheets (Pack of 10)",
        slug="balsa-wood-sheets-pack-10",
        description="Lightweight premium balsa wood sheets for scratch building airframes.",
        technical_specs={"Dimensions": "100x10x0.2 cm", "Material": "Grade AAA Balsa"},
        is_active=True
    )

    ProductVariant.objects.create(
        product=prod2,
        variant_name="2mm Thickness",
        price=450.00,
        sku="BALSA-2MM",
        stock=100
    )
    
    ProductVariant.objects.create(
        product=prod2,
        variant_name="5mm Thickness",
        price=650.00,
        sku="BALSA-5MM",
        stock=75
    )

    print("Products seeded.")

    # 6. Seed Projects
    Project.objects.create(
        title="Autonomous Drone Delivery Core",
        slug="autonomous-drone-delivery",
        category="RESEARCH",
        description="A proof-of-concept for payload delivery capable drones using PX4.",
        client_name="Internal Research",
        completed_date=timezone.now().date(),
        is_active=True
    )

    Project.objects.create(
        title="Solar Powered Glider",
        slug="solar-powered-glider",
        category="DEVELOPMENT",
        description="A 2-meter wingspan glider capable of staying aloft for hours using solar charting.",
        client_name="EcoFlight Ltd",
        completed_date=timezone.now().date() - timedelta(days=30),
        is_active=True
    )

    print("Projects seeded.")
    print("Seeding complete!")

if __name__ == '__main__':
    seed_data()
