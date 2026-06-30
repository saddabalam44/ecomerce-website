from decimal import Decimal
from django.conf import settings
from products.models import Product, ProductVariant
from .models import Cart, CartItem

class SessionCart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.SESSION_COOKIE_NAME + '_cart')
        if not cart:
            cart = self.session[settings.SESSION_COOKIE_NAME + '_cart'] = {}
        self.cart = cart

    def add(self, product, quantity=1, variant_id=None, override_quantity=False):
        product_id = str(product.id)
        key = f"{product_id}_{variant_id}" if variant_id else f"{product_id}_"
        
        if key not in self.cart:
            self.cart[key] = {'quantity': 0, 'price': str(product.final_price), 'variant_id': variant_id}

        if override_quantity:
            self.cart[key]['quantity'] = quantity
        else:
            self.cart[key]['quantity'] += quantity
        self.save()

    def save(self):
        self.session[settings.SESSION_COOKIE_NAME + '_cart'] = self.cart
        self.session.modified = True

    def remove(self, product, variant_id=None):
        product_id = str(product.id)
        key = f"{product_id}_{variant_id}" if variant_id else f"{product_id}_"
        if key in self.cart:
            del self.cart[key]
            self.save()

    def clear(self):
        del self.session[settings.SESSION_COOKIE_NAME + '_cart']
        self.session.modified = True

    def __iter__(self):
        for key, item in self.cart.items():
            product_id, variant_id = key.split('_')
            product = Product.objects.get(id=int(product_id))
            variant = None
            price = Decimal(item['price'])
            
            if variant_id:
                variant = ProductVariant.objects.get(id=int(variant_id))
                if variant.price_override is not None:
                    price = variant.price_override
            
            item['product'] = product
            item['variant'] = variant
            item['price'] = price
            item['total_price'] = price * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def merge_with_database(self, user):
        db_cart, _ = Cart.objects.get_or_create(user=user)
        for key, item in self.cart.items():
            product_id, variant_id_str = key.split('_')
            product = Product.objects.get(id=int(product_id))
            variant = None
            if variant_id_str:
                variant = ProductVariant.objects.get(id=int(variant_id_str))

            cart_item, created = CartItem.objects.get_or_create(
                cart=db_cart,
                product=product,
                variant=variant,
                defaults={'quantity': item['quantity']}
            )
            if not created:
                cart_item.quantity += item['quantity']
                cart_item.save()
        self.clear()
