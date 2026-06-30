from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

from products.views import DRFCategoryViewSet, DRFProductViewSet
from reviews.views import DRFReviewViewSet
from cart.views import DRFCartViewSet
from wishlist.views import DRFWishlistViewSet
from orders.views import DRFOrderViewSet

# Register DRF ViewSets
router = DefaultRouter()
router.register(r'categories', DRFCategoryViewSet, basename='api-category')
router.register(r'products', DRFProductViewSet, basename='api-product')
router.register(r'reviews', DRFReviewViewSet, basename='api-review')
router.register(r'cart', DRFCartViewSet, basename='api-cart')
router.register(r'wishlist', DRFWishlistViewSet, basename='api-wishlist')
router.register(r'orders', DRFOrderViewSet, basename='api-order')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('accounts/', include('accounts.urls')),
    path('products/', include('products.urls')),
    path('cart/', include('cart.urls')),
    path('wishlist/', include('wishlist.urls')),
    path('orders/', include('orders.urls')),
    path('payments/', include('payments.urls')),
    path('reviews/', include('reviews.urls')),
    path('dashboard/', include('dashboard.urls')),
    
    # REST API endpoints
    path('api/', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
