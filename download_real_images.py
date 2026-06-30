import os
import urllib.request
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shopsphere.settings')
django.setup()

from products.models import Product, ProductImage

# High-quality verified Unsplash image links for all 45 products
image_urls = {
    # --- ELECTRONICS (15) ---
    "iphone-15-pro-max": "https://images.unsplash.com/photo-1510557880182-3d4d3cba35a5?w=800&auto=format&fit=crop&q=60",
    "samsung-galaxy-s24-ultra": "https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?w=800&auto=format&fit=crop&q=60",
    "macbook-pro-14-m3": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=800&auto=format&fit=crop&q=60",
    "sony-wh-1000xm5-wireless-headphones": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&auto=format&fit=crop&q=60",
    "nintendo-switch-oled": "https://images.unsplash.com/photo-1606144042614-b2417e99c4e3?w=800&auto=format&fit=crop&q=60",
    "ipad-air": "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=800&auto=format&fit=crop&q=60",
    "apple-watch-9": "https://images.unsplash.com/photo-1542751371-adc38448a05e?w=800&auto=format&fit=crop&q=60",
    "logitech-mx-mouse": "https://images.unsplash.com/photo-1615663245857-ac93bb7c39e7?w=800&auto=format&fit=crop&q=60",
    "logitech-mx-keys": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=800&auto=format&fit=crop&q=60",
    "bose-soundlink-speaker": "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=800&auto=format&fit=crop&q=60",
    "anker-20k-powerbank": "https://images.unsplash.com/photo-1583863788434-e58a36330cf0?w=800&auto=format&fit=crop&q=60",
    "kindle-paperwhite": "https://images.unsplash.com/photo-1543002588-bfa74002ed7e?w=800&auto=format&fit=crop&q=60",
    "dji-mini-drone": "https://images.unsplash.com/photo-1508614589041-895b88991e3e?w=800&auto=format&fit=crop&q=60",
    "gopro-hero12": "https://images.unsplash.com/photo-1502920917128-1aa500764cbd?w=800&auto=format&fit=crop&q=60",
    "xbox-controller": "https://images.unsplash.com/photo-1600080972464-8e5f35f63d08?w=800&auto=format&fit=crop&q=60",

    # --- FASHION (15) ---
    "premium-denim-jacket": "https://images.unsplash.com/photo-1576995853123-5a10305d93c0?w=800&auto=format&fit=crop&q=60",
    "suede-chelsea-boots": "https://images.unsplash.com/photo-1520639888713-7851133b1ed0?w=800&auto=format&fit=crop&q=60",
    "casual-linen-shirt": "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=800&auto=format&fit=crop&q=60",
    "leather-backpack": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=800&auto=format&fit=crop&q=60",
    "polarized-sunglasses": "https://images.unsplash.com/photo-1511499767150-a48a237f0083?w=800&auto=format&fit=crop&q=60",
    "classic-cotton-hoodie": "https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=800&auto=format&fit=crop&q=60",
    "athletic-running-shorts": "https://images.unsplash.com/photo-1539185441755-769473a23570?w=800&auto=format&fit=crop&q=60",
    "slim-fit-chino-pants": "https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?w=800&auto=format&fit=crop&q=60",
    "crewneck-wool-sweater": "https://images.unsplash.com/photo-1614975058789-41316d0e2e9c?w=800&auto=format&fit=crop&q=60",
    "premium-leather-belt": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=800&auto=format&fit=crop&q=60",
    "knit-winter-scarf": "https://images.unsplash.com/photo-1544022613-e87ca75a784a?w=800&auto=format&fit=crop&q=60",
    "baseball-snapback-cap": "https://images.unsplash.com/photo-1588850561407-ed78c282e89b?w=800&auto=format&fit=crop&q=60",
    "canvas-weekend-duffel": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=800&auto=format&fit=crop&q=60",
    "cotton-socks-set": "https://images.unsplash.com/photo-1582966772680-860e372bb558?w=800&auto=format&fit=crop&q=60",
    "windbreaker-running-jacket": "https://images.unsplash.com/photo-1548883354-7622d03aca27?w=800&auto=format&fit=crop&q=60",

    # --- HOME DECOR (15) ---
    "minimalist-silent-wall-clock": "https://images.unsplash.com/photo-1563861826100-9cb868fdbe1c?w=800&auto=format&fit=crop&q=60",
    "ceramic-table-lamp": "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=800&auto=format&fit=crop&q=60",
    "textured-throw-pillow": "https://images.unsplash.com/photo-1584100936595-c0654b55a2e2?w=800&auto=format&fit=crop&q=60",
    "handwoven-area-rug": "https://images.unsplash.com/photo-1600121848594-d8644e57abab?w=800&auto=format&fit=crop&q=60",
    "scented-soy-candle-set": "https://images.unsplash.com/photo-1603006905003-be475563bc59?w=800&auto=format&fit=crop&q=60",
    "terrarium-gold-frame": "https://images.unsplash.com/photo-1545241047-6083a3684587?w=800&auto=format&fit=crop&q=60",
    "nordic-ceramic-vase": "https://images.unsplash.com/photo-1612196808214-b8e1d6145a8c?w=800&auto=format&fit=crop&q=60",
    "brass-picture-frame": "https://images.unsplash.com/photo-1583847268964-b28dc8f51f92?w=800&auto=format&fit=crop&q=60",
    "geometric-floating-shelves": "https://images.unsplash.com/photo-1616486338812-3dadae4b4ace?w=800&auto=format&fit=crop&q=60",
    "macrame-wall-hanging": "https://images.unsplash.com/photo-1528127269322-539801943592?w=800&auto=format&fit=crop&q=60",
    "succulent-planter-set": "https://images.unsplash.com/photo-1485955900006-10f4d324d411?w=800&auto=format&fit=crop&q=60",
    "wooden-desk-organizer": "https://images.unsplash.com/photo-1513151233558-d860c5398176?w=800&auto=format&fit=crop&q=60",
    "scented-reed-diffuser": "https://images.unsplash.com/photo-1540555700478-4be289fbecef?w=800&auto=format&fit=crop&q=60",
    "metal-candle-holders": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=800&auto=format&fit=crop&q=60",
    "abstract-canvas-art": "https://images.unsplash.com/photo-1513519245088-0e12902e5a38?w=800&auto=format&fit=crop&q=60",
}

def download_images():
    dest_dir = r"c:\Users\sadda\OneDrive\Desktop\ecomerce website\media\products"
    os.makedirs(dest_dir, exist_ok=True)
    
    print(f"Downloading high-quality photographic images for all {len(image_urls)} products...")
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    
    for slug, url in image_urls.items():
        filename = f"{slug}.jpg"
        filepath = os.path.join(dest_dir, filename)
        
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as response, open(filepath, 'wb') as out_file:
                out_file.write(response.read())
            print(f"Downloaded photograph for {slug}")
            
            # Associate in database
            product = Product.objects.get(slug=slug)
            ProductImage.objects.filter(product=product).delete()
            ProductImage.objects.create(
                product=product,
                image=f"products/{filename}",
                alt_text=f"High-resolution photo of {product.name}"
            )
        except Exception as e:
            print(f"Failed to download/register image for {slug}: {e}")

if __name__ == '__main__':
    download_images()
