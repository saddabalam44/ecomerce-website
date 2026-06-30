from products.models import Category
from core.models import Notification
from wishlist.models import Wishlist
from cart.views import get_cart_data

def global_context(request):
    categories = Category.objects.filter(parent=None)
    unread_notifications = []
    wishlist_count = 0
    cart_count = 0

    if request.user.is_authenticated:
        unread_notifications = Notification.objects.filter(user=request.user, is_read=False)[:5]
        wishlist_count = Wishlist.objects.filter(user=request.user).count()
        _, _, cart_count = get_cart_data(request)
    else:
        # For anonymous users, get cart count from session
        from cart.cart import SessionCart
        session_cart = SessionCart(request)
        cart_count = len(session_cart)

    return {
        'global_categories': categories,
        'global_notifications': unread_notifications,
        'global_wishlist_count': wishlist_count,
        'global_cart_count': cart_count,
    }
