from rest_framework import serializers
from .models import Order, OrderItem, Coupon
from products.serializers import ProductSerializer

class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ['id', 'code', 'discount_amount', 'discount_type', 'active']

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price', 'variant', 'total_price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    coupon = CouponSerializer(read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'user', 'billing_address', 'shipping_address', 'total_amount', 
            'discount_amount', 'coupon', 'shipping_charge', 'tax', 'final_amount', 
            'status', 'payment_method', 'created_at', 'updated_at', 'items'
        ]
