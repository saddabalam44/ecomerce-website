from django.urls import path
from . import views

app_name = 'wishlist'

urlpatterns = [
    path('', views.wishlist_detail_view, name='wishlist_detail'),
    path('add/<int:product_id>/', views.wishlist_add_view, name='wishlist_add'),
    path('remove/<int:product_id>/', views.wishlist_remove_view, name='wishlist_remove'),
    path('move-to-cart/<int:product_id>/', views.wishlist_move_to_cart_view, name='wishlist_move_to_cart'),
]
