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
    ]
    
    for src_name, slug, dest_name in mappings:
        src_path = os.path.join(artifact_dir, src_name)
        dest_path = os.path.join(dest_dir, dest_name)
        
        if os.path.exists(src_path):
            shutil.copy2(src_path, dest_path)
            print(f"Copied {src_name} to {dest_path}")
            
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
        else:
            print(f"Source file {src_path} does not exist.")

if __name__ == '__main__':
    copy_and_register_images()
