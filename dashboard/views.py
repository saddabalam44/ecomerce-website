from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.db.models import Sum, Count
from django.db.models.functions import TruncDate
from django.utils import timezone
from datetime import timedelta

from orders.models import Order, OrderItem
from products.models import Product, Category, ProductImage
from accounts.models import CustomUser
from .forms import ProductForm

@staff_member_required
def admin_dashboard_view(request):
    # Overall summary stats
    total_revenue = Order.objects.filter(status='PAID').aggregate(total=Sum('final_amount'))['total'] or 0.0
    total_orders = Order.objects.count()
    total_users = CustomUser.objects.count()
    low_stock_products = Product.objects.filter(stock__lte=5)
    out_of_stock_count = Product.objects.filter(stock=0).count()

    # Sales over the last 30 days
    thirty_days_ago = timezone.now() - timedelta(days=30)
    recent_sales = Order.objects.filter(status='PAID', created_at__gte=thirty_days_ago) \
                                .annotate(day=TruncDate('created_at')) \
                                .values('day') \
                                .annotate(total=Sum('final_amount'), count=Count('id')) \
                                .order_by('day')

    # Categories sales share
    category_shares = OrderItem.objects.filter(order__status='PAID') \
                                       .values('product__category__name') \
                                       .annotate(revenue=Sum('price'), sold_count=Sum('quantity')) \
                                       .order_by('-revenue')

    # Recent Orders
    recent_orders = Order.objects.all().order_by('-created_at')[:10]

    return render(request, 'dashboard/dashboard.html', {
        'total_revenue': total_revenue,
        'total_orders': total_orders,
        'total_users': total_users,
        'low_stock_products': low_stock_products,
        'out_of_stock_count': out_of_stock_count,
        'recent_sales': list(recent_sales),
        'category_shares': list(category_shares),
        'recent_orders': recent_orders,
    })

@staff_member_required
def admin_product_list_view(request):
    products = Product.objects.all().order_by('-created_at')
    categories = Category.objects.all()
    form = ProductForm()
    return render(request, 'dashboard/product_list.html', {
        'products': products,
        'categories': categories,
        'form': form,
    })

@staff_member_required
def admin_product_create_view(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            image_file = form.cleaned_data.get('image')
            if image_file:
                ProductImage.objects.create(
                    product=product,
                    image=image_file,
                    alt_text=product.name
                )
            messages.success(request, f"Product '{product.name}' created successfully.")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in field '{field}': {error}")
    return redirect('dashboard:product_list')

@staff_member_required
def admin_product_edit_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save()
            image_file = form.cleaned_data.get('image')
            if image_file:
                # Clean up existing images and replace with the new one
                product.images.all().delete()
                ProductImage.objects.create(
                    product=product,
                    image=image_file,
                    alt_text=product.name
                )
            messages.success(request, f"Product '{product.name}' updated successfully.")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in field '{field}': {error}")
    return redirect('dashboard:product_list')

@staff_member_required
def admin_product_delete_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        name = product.name
        product.delete()
        messages.success(request, f"Product '{name}' deleted successfully.")
    return redirect('dashboard:product_list')

@staff_member_required
def admin_order_list_view(request):
    import datetime
    
    filter_type = request.GET.get('filter_type')
    selected_date_str = request.GET.get('date')
    orders = Order.objects.all()
    
    now = timezone.now()
    today = now.date()
    
    if filter_type == 'today':
        orders = orders.filter(created_at__date=today)
    elif filter_type == 'yesterday':
        yesterday = today - datetime.timedelta(days=1)
        orders = orders.filter(created_at__date=yesterday)
    elif filter_type == 'date' and selected_date_str:
        try:
            selected_date = datetime.datetime.strptime(selected_date_str, '%Y-%m-%d').date()
            orders = orders.filter(created_at__date=selected_date)
        except ValueError:
            pass
            
    orders = orders.order_by('-created_at')
    return render(request, 'dashboard/order_list.html', {'orders': orders})

@staff_member_required
def admin_order_detail_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES):
            old_status = order.status
            order.status = new_status
            order.save()
            
            # If status changed, create a notification for the customer
            if old_status != new_status:
                from core.models import Notification
                Notification.objects.create(
                    user=order.user,
                    message=f"Your Order #{order.id} status has been updated from {old_status} to {new_status}."
                )
            
            messages.success(request, f"Order status updated to {order.get_status_display()} successfully.")
        else:
            messages.error(request, "Invalid status choice.")
        return redirect('dashboard:order_detail', order_id=order.id)

    return render(request, 'dashboard/order_detail.html', {
        'order': order,
        'status_choices': Order.STATUS_CHOICES,
    })

@staff_member_required
def admin_user_list_view(request):
    users = CustomUser.objects.all().order_by('-is_staff', '-date_joined')
    return render(request, 'dashboard/user_list.html', {'users': users})
