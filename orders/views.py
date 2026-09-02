from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, FileResponse
from django.utils import timezone
from django.conf import settings
from decimal import Decimal
import io

from .models import Order, OrderItem, Coupon
from accounts.models import Address
from cart.models import Cart
from products.models import Product

# Invoice generation imports
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

@login_required
def checkout_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    if cart.items.count() == 0:
        messages.error(request, "Your cart is empty. Please add products before checking out.")
        return redirect('cart:cart_detail')

    addresses = request.user.addresses.all()
    subtotal = cart.get_total_price
    
    # Calculate discount
    discount = Decimal('0.00')
    coupon_id = request.session.get('applied_coupon_id')
    coupon = None
    if coupon_id:
        try:
            coupon = Coupon.objects.get(id=coupon_id, active=True, valid_from__lte=timezone.now(), valid_to__gte=timezone.now())
            if coupon.discount_type == 'FIXED':
                discount = coupon.discount_amount
            elif coupon.discount_type == 'PERCENTAGE':
                discount = (subtotal * coupon.discount_amount) / Decimal('100.00')
        except Coupon.DoesNotExist:
            request.session['applied_coupon_id'] = None

    # Calculate shipping (Flat 50, free for orders over 500)
    shipping = Decimal('50.00') if subtotal < Decimal('500.00') else Decimal('0.00')
    
    # Calculate tax (5% of subtotal)
    tax = (subtotal * Decimal('0.05')).quantize(Decimal('0.01'))
    
    # Final total
    final_total = (subtotal - discount + shipping + tax).quantize(Decimal('0.01'))
    if final_total < 0:
        final_total = Decimal('0.00')

    if request.method == 'POST':
        address_id = request.POST.get('shipping_address')
        payment_method = request.POST.get('payment_method')

        if not address_id:
            messages.error(request, "Please select an address.")
            return redirect('orders:checkout')

        if not payment_method:
            messages.error(request, "Please select a payment method.")
            return redirect('orders:checkout')

        address = get_object_or_404(Address, id=address_id, user=request.user)
        
        # Create Order
        order = Order.objects.create(
            user=request.user,
            billing_address=address,
            shipping_address=address,
            total_amount=subtotal,
            discount_amount=discount,
            coupon=coupon,
            shipping_charge=shipping,
            tax=tax,
            final_amount=final_total,
            status='PENDING',
            payment_method=payment_method
        )

        # Create OrderItems
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.unit_price,
                variant=item.variant
            )
            # Deduct stock
            if item.variant:
                item.variant.stock = max(0, item.variant.stock - item.quantity)
                item.variant.save()
            else:
                item.product.stock = max(0, item.product.stock - item.quantity)
                item.product.save()

        # Clear cart and applied coupon
        cart.items.all().delete()
        request.session['applied_coupon_id'] = None

        # Route to Payment Selection or COD
        if payment_method == 'COD':
            order.status = 'PENDING'
            order.save()
            
            # Record cod payment
            from payments.models import Payment
            Payment.objects.create(
                order=order,
                payment_id=f"COD-{order.id}",
                amount=final_total,
                provider='COD',
                status='SUCCESS'  # marked success since order is confirmed
            )
            
            # Send Notification
            from core.models import Notification
            Notification.objects.create(
                user=request.user,
                message=f"Order #{order.id} placed successfully via Cash on Delivery!"
            )
            
            messages.success(request, f"Order #{order.id} placed successfully!")
            return redirect('orders:success', order_id=order.id)
        else:
            return redirect('payments:payment_selection', order_id=order.id)

    return render(request, 'orders/checkout.html', {
        'cart': cart,
        'addresses': addresses,
        'subtotal': subtotal,
        'discount': discount,
        'coupon': coupon,
        'shipping': shipping,
        'tax': tax,
        'final_total': final_total,
    })

def apply_coupon_view(request):
    if request.method == 'POST':
        code = request.POST.get('coupon_code', '').strip()
        cart, _ = Cart.objects.get_or_create(user=request.user)
        subtotal = cart.get_total_price

        try:
            coupon = Coupon.objects.get(code__iexact=code, active=True, valid_from__lte=timezone.now(), valid_to__gte=timezone.now())
            request.session['applied_coupon_id'] = coupon.id
            
            discount = coupon.discount_amount
            if coupon.discount_type == 'PERCENTAGE':
                discount = (subtotal * coupon.discount_amount) / Decimal('100.00')

            return JsonResponse({
                'status': 'success',
                'message': 'Coupon applied successfully!',
                'discount': float(discount.quantize(Decimal('0.01')))
            })
        except Coupon.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid or expired coupon code.'
            })
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

@login_required
def order_success_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/success.html', {'order': order})

@login_required
def order_list_view(request):
    if request.user.is_staff:
        return redirect('dashboard:order_list')
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_list.html', {'orders': orders})

@login_required
def order_detail_view(request, order_id):
    if request.user.is_staff:
        order = get_object_or_404(Order, id=order_id)
    else:
        order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})

@login_required
def cancel_order_view(request, order_id):
    if request.user.is_staff:
        order = get_object_or_404(Order, id=order_id)
    else:
        order = get_object_or_404(Order, id=order_id, user=request.user)
    if order.status in ['PENDING', 'PAID']:
        order.status = 'CANCELLED'
        order.save()
        messages.success(request, f"Order #{order.id} has been cancelled successfully.")
        
        # Create notification
        from core.models import Notification
        Notification.objects.create(
            user=request.user,
            message=f"Order #{order.id} has been cancelled."
        )
    else:
        messages.error(request, "This order cannot be cancelled as it is already shipped/delivered.")
    return redirect('orders:order_detail', order_id=order.id)

@login_required
def return_order_view(request, order_id):
    if request.user.is_staff:
        order = get_object_or_404(Order, id=order_id)
    else:
        order = get_object_or_404(Order, id=order_id, user=request.user)
    if order.status == 'DELIVERED':
        order.status = 'RETURNED'
        order.save()
        messages.success(request, f"Return request for Order #{order.id} submitted.")
        
        from core.models import Notification
        Notification.objects.create(
            user=request.user,
            message=f"Return initiated for Order #{order.id}."
        )
    else:
        messages.error(request, "Only delivered orders can be returned.")
    return redirect('orders:order_detail', order_id=order.id)

@login_required
def generate_invoice_pdf_view(request, order_id):
    if request.user.is_staff:
        order = get_object_or_404(Order, id=order_id)
    else:
        order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # Create the PDF in memory
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    story = []
    
    # Invoice Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'InvoiceTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#0f172a'), # Premium dark slate
        spaceAfter=15
    )
    normal_style = styles['Normal']
    bold_style = ParagraphStyle('BoldText', parent=normal_style, fontName='Helvetica-Bold')

    # Content
    story.append(Paragraph("ShopSphere Invoice", title_style))
    story.append(Paragraph(f"<b>Invoice Date:</b> {timezone.now().strftime('%Y-%m-%d %H:%M')}", normal_style))
    story.append(Paragraph(f"<b>Order Number:</b> #{order.id}", normal_style))
    story.append(Paragraph(f"<b>Billing / Shipping Address:</b><br/>{order.billing_address}", normal_style))
    story.append(Spacer(1, 20))

    # Items table
    data = [['Product', 'Variant', 'Qty', 'Unit Price', 'Total']]
    for item in order.items.all():
        variant_txt = f"{item.variant.name}: {item.variant.value}" if item.variant else "-"
        data.append([
            item.product.name,
            variant_txt,
            str(item.quantity),
            f"₹{item.price}",
            f"₹{item.total_price}"
        ])

    data.append(['', '', '', 'Subtotal:', f"₹{order.total_amount}"])
    if order.discount_amount > 0:
        data.append(['', '', '', 'Discount:', f"-₹{order.discount_amount}"])
    data.append(['', '', '', 'Shipping:', f"₹{order.shipping_charge}"])
    data.append(['', '', '', 'Tax (5%):', f"₹{order.tax}"])
    data.append(['', '', '', 'Total Paid:', f"₹{order.final_amount}"])

    t = Table(data, colWidths=[200, 100, 50, 90, 100])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e293b')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('GRID', (0, 0), (-1, -6), 0.5, colors.grey),
        ('BACKGROUND', (-2, -5), (-1, -1), colors.HexColor('#f8fafc')),
        ('FONTNAME', (-2, -5), (-1, -1), 'Helvetica-Bold'),
        ('ALIGN', (-2, -5), (-1, -1), 'RIGHT'),
    ]))
    story.append(t)
    story.append(Spacer(1, 30))
    story.append(Paragraph("Thank you for shopping with ShopSphere!", bold_style))

    doc.build(story)
    buffer.seek(0)
    
    return FileResponse(buffer, as_attachment=True, filename=f"ShopSphere_Invoice_{order.id}.pdf")


# DRF Order APIs
from rest_framework import viewsets, permissions
from .serializers import OrderSerializer

class DRFOrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

