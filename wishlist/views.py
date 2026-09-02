from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from products.models import Product
from cart.models import Cart, CartItem
from .models import Wishlist

@login_required
def wishlist_detail_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist/wishlist_detail.html', {'wishlist_items': wishlist_items})

@login_required
def wishlist_add_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item = Wishlist.objects.filter(user=request.user, product=product).first()
    
    if wishlist_item:
        wishlist_item.delete()
        msg = "Product removed from wishlist."
        status_msg = "removed"
    else:
        Wishlist.objects.create(user=request.user, product=product)
        msg = "Product added to wishlist."
        status_msg = "added"

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        count = Wishlist.objects.filter(user=request.user).count()
        return JsonResponse({'status': 'success', 'action': status_msg, 'message': msg, 'wishlist_count': count})
        
    messages.success(request, msg)
    return redirect('wishlist:wishlist_detail')

@login_required
def wishlist_remove_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item = Wishlist.objects.filter(user=request.user, product=product).first()
    if wishlist_item:
        wishlist_item.delete()
        msg = "Product removed from wishlist."
    else:
        msg = "Product was not in your wishlist."

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        count = Wishlist.objects.filter(user=request.user).count()
        return JsonResponse({'status': 'success', 'message': msg, 'wishlist_count': count})

    messages.success(request, msg)
    return redirect('wishlist:wishlist_detail')

@login_required
def wishlist_move_to_cart_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Remove from wishlist
    Wishlist.objects.filter(user=request.user, product=product).delete()
    
    # Add to database cart
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'quantity': 1})
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f"Moved {product.name} to your cart.")
    return redirect('wishlist:wishlist_detail')


# DRF Wishlist APIs
from rest_framework import viewsets, permissions
from .serializers import WishlistSerializer

class DRFWishlistViewSet(viewsets.ModelViewSet):
    serializer_class = WishlistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)

