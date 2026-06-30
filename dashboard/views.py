from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta

from orders.models import Order, OrderItem
from products.models import Product, Category
from accounts.models import CustomUser

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
                                .extra(select={'day': "date(created_at)"}) \
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
    return render(request, 'dashboard/product_list.html', {'products': products})

@staff_member_required
def admin_order_list_view(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'dashboard/order_list.html', {'orders': orders})

@staff_member_required
def admin_user_list_view(request):
    users = CustomUser.objects.all().order_by('-date_joined')
    return render(request, 'dashboard/user_list.html', {'users': users})
