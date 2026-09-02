from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.admin_dashboard_view, name='home'),
    path('products/', views.admin_product_list_view, name='product_list'),
    path('products/create/', views.admin_product_create_view, name='product_create'),
    path('products/<int:product_id>/edit/', views.admin_product_edit_view, name='product_edit'),
    path('products/<int:product_id>/delete/', views.admin_product_delete_view, name='product_delete'),
    path('orders/', views.admin_order_list_view, name='order_list'),
    path('orders/<int:order_id>/', views.admin_order_detail_view, name='order_detail'),
    path('users/', views.admin_user_list_view, name='user_list'),
]
