from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.admin_dashboard_view, name='home'),
    path('products/', views.admin_product_list_view, name='product_list'),
    path('orders/', views.admin_order_list_view, name='order_list'),
    path('users/', views.admin_user_list_view, name='user_list'),
]
