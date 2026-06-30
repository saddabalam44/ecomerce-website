import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shopsphere.settings')
django.setup()

from products.models import Category, Product, ProductVariant
from orders.models import Coupon
from django.utils import timezone
from datetime import timedelta

def seed():
    print("Seeding database with premium categories and products...")

    # Create Categories
    electronics, _ = Category.objects.get_or_create(
        name="Electronics",
        slug="electronics",
        description="Premium smartphones, laptops, and gadgets."
    )
    
    fashion, _ = Category.objects.get_or_create(
        name="Fashion",
        slug="fashion",
        description="Trending clothing, jackets, and footwear."
    )
    
    home_decor, _ = Category.objects.get_or_create(
        name="Home Decor",
        slug="home-decor",
        description="Modern home clock, plants, and canvas prints."
    )

    # 1. iPhone 15 Pro Max
    p1, created = Product.objects.get_or_create(
        name="iPhone 15 Pro Max",
        slug="iphone-15-pro-max",
        defaults={
            'description': "Experience the ultimate titanium iPhone with the A17 Pro chip and advanced zoom camera system.",
            'price': 1099.99,
            'discount_price': 999.99,
            'category': electronics,
            'stock': 15,
            'is_featured': True
        }
    )
    if created:
        ProductVariant.objects.create(product=p1, name="Color", value="Natural Titanium", stock=8)
        ProductVariant.objects.create(product=p1, name="Color", value="Blue Titanium", stock=7)

    # 2. Samsung Galaxy S24 Ultra
    p2, created = Product.objects.get_or_create(
        name="Samsung Galaxy S24 Ultra",
        slug="samsung-galaxy-s24-ultra",
        defaults={
            'description': "Unleash creativity and productivity with Galaxy AI, 200MP camera sensor, and built-in S Pen.",
            'price': 1199.99,
            'discount_price': 1079.99,
            'category': electronics,
            'stock': 12,
            'is_featured': True
        }
    )
    if created:
        ProductVariant.objects.create(product=p2, name="Color", value="Titanium Gray", stock=6)
        ProductVariant.objects.create(product=p2, name="Color", value="Titanium Black", stock=6)

    # 3. MacBook Pro 14" M3
    p3, created = Product.objects.get_or_create(
        name="MacBook Pro 14\" M3",
        slug="macbook-pro-14-m3",
        defaults={
            'description': "The 14-inch MacBook Pro blasts forward with the M3 chip, delivering speed, performance, and long battery life.",
            'price': 1599.99,
            'discount_price': 1499.99,
            'category': electronics,
            'stock': 8,
            'is_featured': True
        }
    )
    if created:
        ProductVariant.objects.create(product=p3, name="RAM", value="8GB Unified Memory", stock=4)
        ProductVariant.objects.create(product=p3, name="RAM", value="16GB Unified Memory", stock=4, price_override=1699.99)

    # 4. Sony WH-1000XM5 Wireless Headphones
    p4, created = Product.objects.get_or_create(
        name="Sony WH-1000XM5 Wireless Headphones",
        slug="sony-wh-1000xm5-wireless-headphones",
        defaults={
            'description': "Industry-leading noise canceling headphones with dual processors, 8 microphones, and exceptional call quality.",
            'price': 399.99,
            'discount_price': 349.99,
            'category': electronics,
            'stock': 20,
            'is_featured': False
        }
    )
    if created:
        ProductVariant.objects.create(product=p4, name="Color", value="Silver", stock=10)
        ProductVariant.objects.create(product=p4, name="Color", value="Black", stock=10)

    # 5. Premium Denim Jacket
    p5, created = Product.objects.get_or_create(
        name="Premium Denim Jacket",
        slug="premium-denim-jacket",
        defaults={
            'description': "Classic organic cotton denim jacket featuring double breast pockets, durable metal buttons, and slim-fit cuffs.",
            'price': 89.99,
            'discount_price': 69.99,
            'category': fashion,
            'stock': 25,
            'is_featured': True
        }
    )
    if created:
        ProductVariant.objects.create(product=p5, name="Size", value="Medium", stock=15)
        ProductVariant.objects.create(product=p5, name="Size", value="Large", stock=10)

    # 6. Suede Chelsea Boots
    p6, created = Product.objects.get_or_create(
        name="Suede Chelsea Boots",
        slug="suede-chelsea-boots",
        defaults={
            'description': "Elegant water-resistant tan suede Chelsea boots with flexible elastic side panels and durable crepe rubber soles.",
            'price': 149.99,
            'discount_price': 129.99,
            'category': fashion,
            'stock': 16,
            'is_featured': True
        }
    )
    if created:
        ProductVariant.objects.create(product=p6, name="Size", value="UK 8", stock=8)
        ProductVariant.objects.create(product=p6, name="Size", value="UK 9", stock=8)

    # 7. Casual Linen Shirt
    p7, created = Product.objects.get_or_create(
        name="Casual Linen Shirt",
        slug="casual-linen-shirt",
        defaults={
            'description': "Lightweight breathable 100% linen button-down shirt ideal for summer afternoons or weekend casual getaways.",
            'price': 49.99,
            'category': fashion,
            'stock': 35,
            'is_featured': False
        }
    )
    if created:
        ProductVariant.objects.create(product=p7, name="Size", value="Small", stock=10)
        ProductVariant.objects.create(product=p7, name="Size", value="Medium", stock=15)
        ProductVariant.objects.create(product=p7, name="Size", value="Large", stock=10)

    # 8. Minimalist Silent Wall Clock
    p8, created = Product.objects.get_or_create(
        name="Minimalist Silent Wall Clock",
        slug="minimalist-silent-wall-clock",
        defaults={
            'description': "Modern 12-inch wall clock featuring a matte black finish, quiet sweeping seconds needle, and bold typeface numbers.",
            'price': 45.00,
            'category': home_decor,
            'stock': 30,
            'is_featured': True
        }
    )

    # 9. Ceramic Table Lamp
    p9, created = Product.objects.get_or_create(
        name="Ceramic Table Lamp",
        slug="ceramic-table-lamp",
        defaults={
            'description': "Handcrafted textured oatmeal ceramic lamp base paired with a linen shade, casting warm ambient lighting in any space.",
            'price': 75.00,
            'discount_price': 59.99,
            'category': home_decor,
            'stock': 14,
            'is_featured': False
        }
    )

    # 10. Textured Geometric Throw Pillow
    p10, created = Product.objects.get_or_create(
        name="Textured Throw Pillow",
        slug="textured-throw-pillow",
        defaults={
            'description': "Plush decorative throw pillow featuring woven geometric cotton threads and a soft down feather insert.",
            'price': 29.99,
            'category': home_decor,
            'stock': 40,
            'is_featured': False
        }
    )
    if created:
        ProductVariant.objects.create(product=p10, name="Color", value="Off-White", stock=20)
        ProductVariant.objects.create(product=p10, name="Color", value="Terracotta", stock=20)

    # 11. Handwoven Area Rug
    p11, created = Product.objects.get_or_create(
        name="Handwoven Area Rug",
        slug="handwoven-area-rug",
        defaults={
            'description': "Luxurious soft hand-knotted wool area rug featuring classic neutral lines, adding instant texture and warmth.",
            'price': 249.99,
            'discount_price': 199.99,
            'category': home_decor,
            'stock': 10,
            'is_featured': True
        }
    )

    # Create active coupons
    Coupon.objects.get_or_create(
        code="WELCOME10",
        defaults={
            'discount_amount': 10.00,
            'discount_type': 'PERCENTAGE',
            'active': True,
            'valid_from': timezone.now() - timedelta(days=1),
            'valid_to': timezone.now() + timedelta(days=30)
        }
    )
    
    Coupon.objects.get_or_create(
        code="FLAT50",
        defaults={
            'discount_amount': 50.00,
            'discount_type': 'FIXED',
            'active': True,
            'valid_from': timezone.now() - timedelta(days=1),
            'valid_to': timezone.now() + timedelta(days=30)
        }
    )

    print("Database seeding completed successfully!")

if __name__ == '__main__':
    seed()
