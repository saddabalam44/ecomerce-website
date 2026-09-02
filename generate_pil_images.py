import os
import django
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shopsphere.settings')
django.setup()

from products.models import Product, ProductImage

def create_gradient_background(width, height, color1, color2):
    """Create a beautiful linear gradient image."""
    base = Image.new('RGB', (width, height), color1)
    top = Image.new('RGB', (width, height), color2)
    mask = Image.new('L', (width, height))
    mask_data = []
    for y in range(height):
        # Linear transition from top to bottom
        mask_data.extend([int(255 * (y / height))] * width)
    mask.putdata(mask_data)
    base.paste(top, (0, 0), mask)
    return base

def draw_accent_shapes(img, draw, color):
    """Draw subtle geometric shapes in the background for a modern look."""
    w, h = img.size
    # Subtle circular grid
    for r in range(50, 300, 50):
        draw.ellipse([w//2 - r, h//2 - r, w//2 + r, h//2 + r], outline=color, width=1)
    
    # Diagonal accent lines
    draw.line([0, 0, w, h], fill=color, width=1)
    draw.line([0, h, w, 0], fill=color, width=1)

def generate_product_image(product):
    """Generate a premium stylized card image for a product using PIL."""
    w, h = 800, 600
    category_slug = product.category.slug
    
    # Select color palettes based on category
    if category_slug == 'electronics':
        # Deep technological blues and dark slates
        c1 = (15, 23, 42)      # Slate 900
        c2 = (30, 41, 59)      # Slate 800
        accent = (56, 189, 248, 40)  # Cyan light accent
        text_color = (255, 255, 255)
        sub_text_color = (125, 211, 252) # Cyan 300
    elif category_slug == 'fashion':
        # Warm, organic terracotta and soft sandy earth tones
        c1 = (69, 26, 3)       # Warm Brown
        c2 = (120, 53, 4)      # Terracotta Dark
        accent = (251, 191, 36, 40)   # Gold light accent
        text_color = (255, 255, 255)
        sub_text_color = (252, 211, 77) # Amber 300
    else:
        # Elegant sage greens and muted emerald decors
        c1 = (6, 78, 59)       # Emerald Dark
        c2 = (16, 185, 129)    # Emerald Soft
        accent = (167, 243, 208, 45) # Sage accent
        text_color = (255, 255, 255)
        sub_text_color = (209, 250, 229) # Sage light
        
    img = create_gradient_background(w, h, c1, c2)
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # Draw micro-grid accents
    draw_accent_shapes(img, draw, accent)
    
    # Add shadow/glow layer for text readability
    shadow = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    sh_draw = ImageDraw.Draw(shadow)
    
    # Load windows standard font
    font_path = "C:\\Windows\\Fonts\\segoeui.ttf"
    if not os.path.exists(font_path):
        font_path = "C:\\Windows\\Fonts\\arial.ttf"
        
    try:
        title_font = ImageFont.truetype(font_path, 42)
        tag_font = ImageFont.truetype(font_path, 22)
        price_font = ImageFont.truetype(font_path, 30)
    except IOError:
        # Fallback to default
        title_font = ImageFont.load_default()
        tag_font = ImageFont.load_default()
        price_font = ImageFont.load_default()

    # Draw Category Tag
    tag_text = product.category.name.upper()
    sh_draw.text((w // 2, 80), tag_text, fill=sub_text_color, font=tag_font, anchor="mm")
    
    # Wrap text if title is too long
    words = product.name.split()
    lines = []
    current_line = []
    for word in words:
        current_line.append(word)
        # Check size of line
        test_line = " ".join(current_line)
        bbox = draw.textbbox((0, 0), test_line, font=title_font)
        line_w = bbox[2] - bbox[0]
        if line_w > w - 100:
            current_line.pop()
            lines.append(" ".join(current_line))
            current_line = [word]
    if current_line:
        lines.append(" ".join(current_line))
        
    # Draw product title lines
    start_y = h // 2 - (len(lines) - 1) * 30
    for idx, line in enumerate(lines):
        line_y = start_y + idx * 60
        # Draw dark shadow
        sh_draw.text((w // 2 + 3, line_y + 3), line, fill=(0, 0, 0, 150), font=title_font, anchor="mm")
        # Draw clean main text
        sh_draw.text((w // 2, line_y), line, fill=text_color, font=title_font, anchor="mm")

    # Draw Price Tag at bottom
    price_text = f"₹{product.price}"
    if product.discount_price:
        price_text = f"₹{product.discount_price} (was ₹{product.price})"
    sh_draw.text((w // 2, h - 100), price_text, fill=(255, 255, 255, 220), font=price_font, anchor="mm")

    # Composite the main text onto the image
    img = Image.alpha_composite(img.convert('RGBA'), shadow)
    
    # Save the image
    dest_dir = r"c:\Users\sadda\OneDrive\Desktop\ecomerce website\media\products"
    os.makedirs(dest_dir, exist_ok=True)
    filename = f"{product.slug}.png"
    img_path = os.path.join(dest_dir, filename)
    img.convert('RGB').save(img_path, 'PNG')
    
    # Register in DB
    ProductImage.objects.filter(product=product).delete()
    ProductImage.objects.create(
        product=product,
        image=f"products/{filename}",
        alt_text=f"Premium unique card art for {product.name}"
    )
    print(f"Generated and registered unique PIL image for: {product.name}")

def main():
    products = Product.objects.all()
    print(f"Generating unique PIL images for all {products.count()} products in catalog...")
    for product in products:
        generate_product_image(product)
    print("All unique images generated and database registered successfully!")

if __name__ == '__main__':
    main()
