from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from products.models import Product, ProductVariant
from .models import Cart, CartItem
from .cart import SessionCart

def get_cart_data(request):
    """Helper to retrieve cart items, count, and totals regardless of login status."""
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        items = []
        for db_item in cart.items.all():
            items.append({
                'id': db_item.id,
                'product': db_item.product,
                'variant': db_item.variant,
                'quantity': db_item.quantity,
                'unit_price': db_item.unit_price,
                'total_price': db_item.total_price,
            })
        total_price = cart.get_total_price
        total_items = cart.get_total_items
    else:
        session_cart = SessionCart(request)
        items = list(session_cart)
        total_price = session_cart.get_total_price()
        total_items = len(session_cart)
    
    return items, total_price, total_items

def cart_detail_view(request):
    items, total_price, total_items = get_cart_data(request)
    return render(request, 'cart/cart_detail.html', {
        'items': items,
        'total_price': total_price,
        'total_items': total_items,
    })

def cart_add_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    variant_id = request.POST.get('variant_id')
    variant = None
    if variant_id:
        variant = get_object_or_404(ProductVariant, id=variant_id, product=product)

    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            variant=variant,
            defaults={'quantity': quantity}
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
    else:
        session_cart = SessionCart(request)
        session_cart.add(product, quantity=quantity, variant_id=variant.id if variant else None)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        _, _, total_items = get_cart_data(request)
        return JsonResponse({'status': 'success', 'total_items': total_items, 'message': 'Product added to cart'})
        
    return redirect('cart:cart_detail')

def cart_update_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    variant_id = request.POST.get('variant_id')
    variant = None
    if variant_id:
        variant = get_object_or_404(ProductVariant, id=variant_id, product=product)

    if request.user.is_authenticated:
        cart = get_object_or_404(Cart, user=request.user)
        cart_item = get_object_or_404(CartItem, cart=cart, product=product, variant=variant)
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()
    else:
        session_cart = SessionCart(request)
        if quantity > 0:
            session_cart.add(product, quantity=quantity, variant_id=variant.id if variant else None, override_quantity=True)
        else:
            session_cart.remove(product, variant_id=variant.id if variant else None)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        items, total_price, total_items = get_cart_data(request)
        return JsonResponse({
            'status': 'success',
            'total_items': total_items,
            'total_price': float(total_price),
            'message': 'Cart updated'
        })

    return redirect('cart:cart_detail')

def cart_remove_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    variant_id = request.POST.get('variant_id')
    variant = None
    if variant_id:
        variant = get_object_or_404(ProductVariant, id=variant_id, product=product)

    if request.user.is_authenticated:
        cart = get_object_or_404(Cart, user=request.user)
        cart_item = get_object_or_404(CartItem, cart=cart, product=product, variant=variant)
        cart_item.delete()
    else:
        session_cart = SessionCart(request)
        session_cart.remove(product, variant_id=variant.id if variant else None)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        _, total_price, total_items = get_cart_data(request)
        return JsonResponse({
            'status': 'success',
            'total_items': total_items,
            'total_price': float(total_price),
            'message': 'Product removed from cart'
        })

    return redirect('cart:cart_detail')


# DRF Cart APIs
from rest_framework import viewsets, permissions
from .serializers import CartSerializer

class DRFCartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

