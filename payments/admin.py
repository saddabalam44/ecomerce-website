from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['order', 'payment_id', 'amount', 'provider', 'status', 'created_at']
    list_filter = ['provider', 'status', 'created_at']
    search_fields = ['payment_id', 'order__id']
