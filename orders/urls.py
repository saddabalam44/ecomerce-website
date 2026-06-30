from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('checkout/', views.checkout_view, name='checkout'),
    path('apply-coupon/', views.apply_coupon_view, name='apply_coupon'),
    path('success/<int:order_id>/', views.order_success_view, name='success'),
    path('history/', views.order_list_view, name='order_list'),
    path('<int:order_id>/', views.order_detail_view, name='order_detail'),
    path('<int:order_id>/cancel/', views.cancel_order_view, name='cancel_order'),
    path('<int:order_id>/return/', views.return_order_view, name='return_order'),
    path('<int:order_id>/invoice/', views.generate_invoice_pdf_view, name='generate_invoice'),
]
