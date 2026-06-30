from decimal import Decimal
import pytest
from products.models import Category, Product

@pytest.mark.django_db
def test_category_slugify_logic():
    cat = Category.objects.create(
        name="Laptops & Accessories",
        description="Premium computers"
    )
    assert cat.slug == "laptops-accessories"
    assert str(cat) == "Laptops & Accessories"

@pytest.mark.django_db
def test_product_final_price():
    cat = Category.objects.create(name="Clothing")
    
    # Product without discount
    p1 = Product.objects.create(
        name="Plain T-Shirt",
        description="A plain cotton t-shirt",
        price="19.99",
        category=cat,
        stock=50
    )
    assert Decimal(p1.final_price) == Decimal('19.99')
    
    # Product with discount
    p2 = Product.objects.create(
        name="Designer Jeans",
        description="Denim jeans",
        price="99.99",
        discount_price="79.99",
        category=cat,
        stock=20
    )
    assert Decimal(p2.final_price) == Decimal('79.99')

