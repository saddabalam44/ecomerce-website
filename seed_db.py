import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shopsphere.settings')
django.setup()

from products.models import Category, Product, ProductVariant
from orders.models import Coupon
from django.utils import timezone
from datetime import timedelta

def seed():
    print("Seeding database with premium categories and 45 products...")

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

    # ==================== ELECTRONICS (15 Products) ====================
    e_products = [
        ("iPhone 15 Pro Max", "iphone-15-pro-max", "Experience the ultimate titanium iPhone with the A17 Pro chip and advanced zoom camera system.", 1099.99, 999.99, 15, True),
        ("Samsung Galaxy S24 Ultra", "samsung-galaxy-s24-ultra", "Unleash creativity and productivity with Galaxy AI, 200MP camera sensor, and built-in S Pen.", 1199.99, 1079.99, 12, True),
        ("MacBook Pro 14\" M3", "macbook-pro-14-m3", "The 14-inch MacBook Pro blasts forward with the M3 chip, delivering speed, performance, and long battery life.", 1599.99, 1499.99, 8, True),
        ("Sony WH-1000XM5 Wireless Headphones", "sony-wh-1000xm5-wireless-headphones", "Industry-leading noise canceling headphones with dual processors, 8 microphones, and exceptional call quality.", 399.99, 349.99, 20, False),
        ("Nintendo Switch OLED", "nintendo-switch-oled", "Play on a vibrant 7-inch OLED screen with the Nintendo Switch system in TV, tabletop, or handheld modes.", 349.99, None, 15, True),
        ("Apple iPad Air", "ipad-air", "Light, thin, and powerful iPad Air with the M2 chip, a stunning Liquid Retina display, and superfast Wi-Fi.", 599.99, 549.99, 10, False),
        ("Apple Watch Series 9", "apple-watch-9", "A smarter, brighter, and faster Apple Watch featuring the S9 SiP chip and double tap gesture control.", 399.99, None, 14, False),
        ("Logitech MX Master 3S Mouse", "logitech-mx-mouse", "Ergonomic wireless mouse with 8K DPI tracking on any surface and quiet click buttons.", 99.99, 89.99, 25, False),
        ("Logitech MX Keys Keyboard", "logitech-mx-keys", "Advanced illuminated wireless keyboard featuring fluid keystrokes and smart backlighting.", 119.99, 109.99, 20, False),
        ("Bose SoundLink Flex Speaker", "bose-soundlink-speaker", "Portable waterproof outdoor bluetooth speaker with clear, crisp sound and PositionIQ technology.", 149.99, None, 30, False),
        ("Anker 20K Power Bank", "anker-20k-powerbank", "High-speed charging portable charger pack with 20000mAh capacity and dual USB-C ports.", 49.99, 39.99, 45, False),
        ("Kindle Paperwhite", "kindle-paperwhite", "6.8-inch display screen e-reader with adjustable warm light and up to 10 weeks of battery life.", 139.99, 129.99, 18, False),
        ("DJI Mini 4 Pro Drone", "dji-mini-drone", "Lightweight mini camera drone weighing less than 249g with active obstacle sensing and 4K HDR video.", 759.00, 699.00, 5, False),
        ("GoPro HERO12 Black", "gopro-hero12", "Waterproof action camera with high dynamic range 5.3K video resolution and HyperSmooth stabilization.", 399.00, 349.00, 15, False),
        ("Xbox Wireless Controller", "xbox-controller", "Experience the modernized design of the Xbox wireless controller featuring sculpted surfaces and geometry.", 59.99, 49.99, 40, False),
    ]

    for name, slug, desc, price, disc_price, stock, featured in e_products:
        Product.objects.get_or_create(
            name=name,
            slug=slug,
            defaults={
                'description': desc,
                'price': price,
                'discount_price': disc_price,
                'category': electronics,
                'stock': stock,
                'is_featured': featured
            }
        )

    # ==================== FASHION (15 Products) ====================
    f_products = [
        ("Premium Denim Jacket", "premium-denim-jacket", "Classic organic cotton denim jacket featuring double breast pockets, durable metal buttons, and slim-fit cuffs.", 89.99, 69.99, 25, True),
        ("Suede Chelsea Boots", "suede-chelsea-boots", "Elegant water-resistant tan suede Chelsea boots with flexible elastic side panels and durable crepe rubber soles.", 149.99, 129.99, 16, True),
        ("Casual Linen Shirt", "casual-linen-shirt", "Lightweight breathable 100% linen button-down shirt ideal for summer afternoons or weekend casual getaways.", 49.99, None, 35, False),
        ("Leather Backpack", "leather-backpack", "Handcrafted full-grain leather backpack featuring vintage brass buckles, multiple zipper pouches, and soft padded laptop sleeve.", 199.99, 169.99, 10, True),
        ("Polarized Sunglasses", "polarized-sunglasses", "Classic unisex polarized sunglasses with UV400 protective lenses, reinforced metal hinges, and sleek acetate frames.", 79.99, 59.99, 25, False),
        ("Classic Cotton Hoodie", "classic-cotton-hoodie", "Comfortable soft-brushed cotton blend hoodie with front kangaroo pocket and adjustable drawstring hood.", 59.99, 49.99, 30, False),
        ("Athletic Running Shorts", "athletic-running-shorts", "Lightweight moisture-wicking active shorts with breathable mesh liner and secure back zip pocket.", 29.99, None, 40, False),
        ("Slim-Fit Chino Pants", "slim-fit-chino-pants", "Versatile stretch cotton chino pants with a clean flat front, perfect for semi-formal or daily wear.", 69.99, 59.99, 28, False),
        ("Crewneck Wool Sweater", "crewneck-wool-sweater", "Warm fine-knit merino wool crewneck sweater offering exceptional softness, warmth, and layering capability.", 89.99, 79.99, 20, False),
        ("Premium Leather Belt", "premium-leather-belt", "Classic full-grain genuine leather belt featuring a polished silver-finish buckle, perfect for work or casual settings.", 39.99, None, 50, False),
        ("Knit Winter Scarf", "knit-winter-scarf", "Soft cozy acrylic knit winter scarf featuring a classic ribbed texture to keep you warm on chilly days.", 24.99, 19.99, 60, False),
        ("Baseball Snapback Cap", "baseball-snapback-cap", "Classic 6-panel structured snapback baseball cap with adjustable strap and breathable eyelets.", 19.99, None, 100, False),
        ("Canvas Weekend Duffel", "canvas-weekend-duffel", "Heavyweight water-resistant canvas duffel bag featuring leather handles and a removable shoulder strap.", 129.99, 99.99, 15, False),
        ("Cotton Cushion Socks Set", "cotton-socks-set", "Pack of five comfortable ribbed cotton crew socks with cushioned soles and reinforced heels.", 14.99, None, 120, False),
        ("Windbreaker Running Jacket", "windbreaker-running-jacket", "Water-resistant lightweight nylon windbreaker featuring a packable hood and elastic wrist storm cuffs.", 79.99, 69.99, 22, False),
    ]

    for name, slug, desc, price, disc_price, stock, featured in f_products:
        Product.objects.get_or_create(
            name=name,
            slug=slug,
            defaults={
                'description': desc,
                'price': price,
                'discount_price': disc_price,
                'category': fashion,
                'stock': stock,
                'is_featured': featured
            }
        )

    # ==================== HOME DECOR (15 Products) ====================
    hd_products = [
        ("Minimalist Silent Wall Clock", "minimalist-silent-wall-clock", "Modern 12-inch wall clock featuring a matte black finish, quiet sweeping seconds needle, and bold typeface numbers.", 45.00, None, 30, True),
        ("Ceramic Table Lamp", "ceramic-table-lamp", "Handcrafted textured oatmeal ceramic lamp base paired with a linen shade, casting warm ambient lighting in any space.", 75.00, 59.99, 14, False),
        ("Textured Throw Pillow", "textured-throw-pillow", "Plush decorative throw pillow featuring woven geometric cotton threads and a soft down feather insert.", 29.99, None, 40, False),
        ("Handwoven Area Rug", "handwoven-area-rug", "Luxurious soft hand-knotted wool area rug featuring classic neutral lines, adding instant texture and warmth.", 249.99, 199.99, 10, True),
        ("Scented Soy Candle Set", "scented-soy-candle-set", "Set of three premium hand-poured soy candles infused with lavender, sandalwood, and sage essential oils.", 35.00, None, 50, False),
        ("Terrarium Gold Frame", "terrarium-gold-frame", "Modern geometric glass terrarium with brass frame, ideal for air plants, moss, and small succulents.", 55.00, 45.00, 15, False),
        ("Nordic Ceramic Vase", "nordic-ceramic-vase", "Elegant minimalist white ceramic flower vase with a textured matte finish, perfect for dried stems.", 32.00, 24.99, 25, False),
        ("Brass Picture Frame", "brass-picture-frame", "Modern thin brass metal photo frame with double floating glass sheets, fits standard 5x7 prints.", 28.00, None, 30, False),
        ("Geometric Floating Shelves", "geometric-floating-shelves", "Set of three wall-mounted hexagonal wooden shelves with black iron frames for display.", 48.00, 39.99, 18, False),
        ("Macrame Wall Hanging", "macrame-wall-hanging", "Bohemian hand-woven cotton macrame wall tapestry on a natural wooden dowel, adding cozy texture.", 39.99, None, 20, False),
        ("Succulent Planter Set", "succulent-planter-set", "Trio of small glazed ceramic indoor flower pots with drainage holes and bamboo saucers.", 22.00, 17.99, 35, False),
        ("Wooden Desk Organizer", "wooden-desk-organizer", "Multifunctional bamboo desk tray organizer featuring pen holder compartments and phone dock slot.", 34.99, None, 40, False),
        ("Scented Reed Diffuser", "scented-reed-diffuser", "Aromatic jasmine and vanilla essential oil diffuser in a glass bottle with eight premium reeds.", 26.00, 19.99, 45, False),
        ("Metal Candle Holders", "metal-candle-holders", "Set of three modern sleek matte black taper candle holders of varying heights for table centerpieces.", 42.00, 34.00, 15, False),
        ("Framed Abstract Canvas Art", "abstract-canvas-art", "Modern abstract graphic print on textured canvas, pre-mounted in a thin light oak wood frame.", 89.99, 74.99, 10, True),
    ]

    for name, slug, desc, price, disc_price, stock, featured in hd_products:
        Product.objects.get_or_create(
            name=name,
            slug=slug,
            defaults={
                'description': desc,
                'price': price,
                'discount_price': disc_price,
                'category': home_decor,
                'stock': stock,
                'is_featured': featured
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
