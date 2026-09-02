import stripe
import razorpay
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.urls import reverse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from orders.models import Order
from .models import Payment
from core.models import Notification

# Initialize Razorpay Client if keys are available
try:
    razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
except Exception:
    razorpay_client = None

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def payment_selection_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if order.status != 'PENDING':
        messages.warning(request, "This order is already processed.")
        return redirect('orders:order_detail', order_id=order.id)

    return render(request, 'payments/payment_selection.html', {
        'order': order,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
    })

@login_required
def stripe_checkout_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    # Mock Stripe mode for local development
    if settings.STRIPE_SECRET_KEY == 'sk_test_mock':
        return render(request, 'payments/stripe_mock.html', {'order': order})

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'inr',
                    'product_data': {
                        'name': f"Order #{order.id} on ShopSphere",
                    },
                    'unit_amount': int(order.final_amount * 100),  # cents
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri(
                reverse('payments:stripe_success') + f"?session_id={{CHECKOUT_SESSION_ID}}&order_id={order.id}"
            ),
            cancel_url=request.build_absolute_uri(
                reverse('payments:stripe_cancel') + f"?order_id={order.id}"
            ),
        )
        return redirect(checkout_session.url, code=303)
    except Exception as e:
        messages.error(request, f"Stripe integration error: {e}")
        return redirect('payments:payment_selection', order_id=order.id)

@login_required
def stripe_success_view(request):
    order_id = request.GET.get('order_id')
    order = get_object_or_404(Order, id=order_id, user=request.user)
    session_id = request.GET.get('session_id')

    order.status = 'PAID'
    order.save()

    Payment.objects.update_or_create(
        order=order,
        defaults={
            'payment_id': session_id or f"mock-stripe-{order.id}",
            'amount': order.final_amount,
            'provider': 'STRIPE',
            'status': 'SUCCESS'
        }
    )

    Notification.objects.create(
        user=request.user,
        message=f"Payment for Order #{order.id} verified successfully via Stripe!"
    )

    messages.success(request, f"Payment successful! Order #{order.id} is confirmed.")
    return redirect('orders:success', order_id=order.id)

@login_required
def stripe_cancel_view(request):
    order_id = request.GET.get('order_id')
    order = get_object_or_404(Order, id=order_id, user=request.user)
    messages.error(request, "Stripe payment was cancelled.")
    return redirect('payments:payment_selection', order_id=order.id)

@login_required
def razorpay_checkout_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # Mock Razorpay mode for local development
    if settings.RAZORPAY_KEY_ID == 'rzp_test_mock' or not razorpay_client:
        return render(request, 'payments/razorpay_mock.html', {'order': order})
        
    try:
        # Create Razorpay order
        notes = {'order_id': order.id, 'user': request.user.email}
        razorpay_order = razorpay_client.order.create(dict(
            amount=int(order.final_amount * 100),  # paise
            currency='INR',
            payment_capture='1',
            notes=notes
        ))
        
        context = {
            'order': order,
            'razorpay_order_id': razorpay_order['id'],
            'razorpay_key_id': settings.RAZORPAY_KEY_ID,
            'amount_paise': razorpay_order['amount'],
            'callback_url': request.build_absolute_uri(reverse('payments:razorpay_callback')),
        }
        return render(request, 'payments/razorpay_checkout.html', context)
    except Exception as e:
        messages.error(request, f"Razorpay integration error: {e}")
        return redirect('payments:payment_selection', order_id=order.id)

@csrf_exempt
def razorpay_callback_view(request):
    if request.method == "POST":
        payment_id = request.POST.get('razorpay_payment_id')
        razorpay_order_id = request.POST.get('razorpay_order_id')
        signature = request.POST.get('razorpay_signature')
        order_id = request.POST.get('order_id')
        
        order = get_object_or_404(Order, id=order_id)
        
        # In mock payment mode
        if settings.RAZORPAY_KEY_ID == 'rzp_test_mock' or not razorpay_client:
            order.status = 'PAID'
            order.save()
            
            Payment.objects.update_or_create(
                order=order,
                defaults={
                    'payment_id': payment_id or f"mock-razorpay-{order.id}",
                    'amount': order.final_amount,
                    'provider': 'RAZORPAY',
                    'status': 'SUCCESS'
                }
            )
            return redirect('orders:success', order_id=order.id)

        # Verification of Signature
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }
        try:
            razorpay_client.utility.verify_payment_signature(params_dict)
            # Signature matches
            order.status = 'PAID'
            order.save()
            
            Payment.objects.update_or_create(
                order=order,
                defaults={
                    'payment_id': payment_id,
                    'amount': order.final_amount,
                    'provider': 'RAZORPAY',
                    'status': 'SUCCESS'
                }
            )
            Notification.objects.create(
                user=order.user,
                message=f"Payment for Order #{order.id} verified successfully via Razorpay!"
            )
            messages.success(request, f"Payment successful! Order #{order.id} confirmed.")
            return redirect('orders:success', order_id=order.id)
        except Exception:
            messages.error(request, "Razorpay payment verification failed.")
            return redirect('payments:payment_selection', order_id=order.id)
            
    return HttpResponse("Method not allowed", status=405)
