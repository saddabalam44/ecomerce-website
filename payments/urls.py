from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('select/<int:order_id>/', views.payment_selection_view, name='payment_selection'),
    path('stripe/<int:order_id>/', views.stripe_checkout_view, name='stripe_checkout'),
    path('stripe/success/', views.stripe_success_view, name='stripe_success'),
    path('stripe/cancel/', views.stripe_cancel_view, name='stripe_cancel'),
    path('razorpay/<int:order_id>/', views.razorpay_checkout_view, name='razorpay_checkout'),
    path('razorpay/callback/', views.razorpay_callback_view, name='razorpay_callback'),
]
