import os
import shutil
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shopsphere.settings')
django.setup()

from products.models import Product, ProductImage

def copy_and_register_images():
    print("Copying generated images to media and registering in DB...")
    
    # Source paths
    artifact_dir = r"C:\Users\sadda\.gemini\antigravity-ide\brain\0e0d15d4-7305-4eb4-97fa-303c2d01e686"
    dest_dir = r"c:\Users\sadda\OneDrive\Desktop\ecomerce website\media\products"
    
    os.makedirs(dest_dir, exist_ok=True)
    
    # Mappings of filenames to slugs
    mappings = [
        # Base/Seeded images
        ("iphone_product_1782840440898.png", "iphone-15-pro-max", "iphone.png"),
        ("samsung_product_1782840978036.png", "samsung-galaxy-s24-ultra", "samsung.png"),
        ("macbook_product_1782840455052.png", "macbook-pro-14-m3", "macbook.png"),
        ("headphones_product_1782840467510.png", "sony-wh-1000xm5-wireless-headphones", "headphones.png"),
        ("boots_product_1782840484498.png", "suede-chelsea-boots", "boots.png"),
        ("shirt_product_1782840990742.png", "casual-linen-shirt", "shirt.png"),
        ("denim_product_1782841002484.png", "premium-denim-jacket", "denim.png"),
        ("rug_product_1782841017147.png", "handwoven-area-rug", "rug.png"),
        ("pillow_product_1782841030479.png", "textured-throw-pillow", "pillow.png"),
        ("lamp_product_1782841042446.png", "ceramic-table-lamp", "lamp.png"),
        ("nintendo_product_1782841248939.png", "nintendo-switch-oled", "nintendo.png"),
        ("backpack_product_1782841261382.png", "leather-backpack", "backpack.png"),
        ("sunglasses_product_1782841273812.png", "polarized-sunglasses", "sunglasses.png"),
        ("candle_product_1782841286332.png", "scented-soy-candle-set", "candle.png"),
        ("terrarium_product_1782841299075.png", "terrarium-gold-frame", "terrarium.png"),
        ("clock_product_1782841566853.png", "minimalist-silent-wall-clock", "clock.png"),

        # --- ELECTRONICS MAPPINGS ---
        ("macbook_product_1782840455052.png", "ipad-air", "macbook.png"),
        ("samsung_product_1782840978036.png", "apple-watch-9", "samsung.png"),
        ("headphones_product_1782840467510.png", "logitech-mx-mouse", "headphones.png"),
        ("macbook_product_1782840455052.png", "logitech-mx-keys", "macbook.png"),
        ("headphones_product_1782840467510.png", "bose-soundlink-speaker", "headphones.png"),
        ("iphone_product_1782840440898.png", "anker-20k-powerbank", "iphone.png"),
        ("iphone_product_1782840440898.png", "kindle-paperwhite", "iphone.png"),
        ("nintendo_product_1782841248939.png", "dji-mini-drone", "nintendo.png"),
        ("nintendo_product_1782841248939.png", "gopro-hero12", "nintendo.png"),
        ("nintendo_product_1782841248939.png", "xbox-controller", "nintendo.png"),

        # --- FASHION MAPPINGS ---
        ("denim_product_1782841002484.png", "classic-cotton-hoodie", "denim.png"),
        ("shirt_product_1782840990742.png", "athletic-running-shorts", "shirt.png"),
        ("denim_product_1782841002484.png", "slim-fit-chino-pants", "denim.png"),
        ("shirt_product_1782840990742.png", "crewneck-wool-sweater", "shirt.png"),
        ("boots_product_1782840484498.png", "premium-leather-belt", "boots.png"),
        ("shirt_product_1782840990742.png", "knit-winter-scarf", "shirt.png"),
        ("sunglasses_product_1782841273812.png", "baseball-snapback-cap", "sunglasses.png"),
        ("backpack_product_1782841261382.png", "canvas-weekend-duffel", "backpack.png"),
        ("shirt_product_1782840990742.png", "cotton-socks-set", "shirt.png"),
        ("denim_product_1782841002484.png", "windbreaker-running-jacket", "denim.png"),

        # --- HOME DECOR MAPPINGS ---
        ("lamp_product_1782841042446.png", "nordic-ceramic-vase", "lamp.png"),
        ("clock_product_1782841566853.png", "brass-picture-frame", "clock.png"),
        ("clock_product_1782841566853.png", "geometric-floating-shelves", "clock.png"),
        ("rug_product_1782841017147.png", "macrame-wall-hanging", "rug.png"),
        ("terrarium_product_1782841299075.png", "succulent-planter-set", "terrarium.png"),
        ("clock_product_1782841566853.png", "wooden-desk-organizer", "clock.png"),
        ("candle_product_1782841286332.png", "scented-reed-diffuser", "candle.png"),
        ("candle_product_1782841286332.png", "metal-candle-holders", "candle.png"),
        ("rug_product_1782841017147.png", "abstract-canvas-art", "rug.png"),
    ]
    
    for src_name, slug, dest_name in mappings:
        src_path = os.path.join(artifact_dir, src_name)
        dest_path = os.path.join(dest_dir, dest_name)
        
        # If destination file already exists (from another mapping), we can directly link it in DB.
        # But copy it anyway if source exists to be safe.
        if os.path.exists(src_path):
            shutil.copy2(src_path, dest_path)
            
        # Associate in database
        try:
            product = Product.objects.get(slug=slug)
            # Clear previous images to avoid duplicates
            ProductImage.objects.filter(product=product).delete()
            # Create new entry
            ProductImage.objects.create(
                product=product,
                image=f"products/{dest_name}",
                alt_text=f"Product photo for {product.name}"
            )
            print(f"Registered image for {product.name} in DB.")
        except Product.DoesNotExist:
            print(f"Product with slug '{slug}' not found in database.")

if __name__ == '__main__':
    copy_and_register_images()
