from django.db import models
from orders.models import Order

class Payment(models.Model):
    PROVIDER_CHOICES = (
        ('COD', 'Cash on Delivery'),
        ('STRIPE', 'Stripe'),
        ('RAZORPAY', 'Razorpay'),
    )
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
    )
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment_details')
    payment_id = models.CharField(max_length=255, blank=True, null=True) # Stripe/Razorpay payment intent id
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    provider = models.CharField(max_length=20, choices=PROVIDER_CHOICES, default='COD')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for Order #{self.order.id} via {self.provider} ({self.status})"
