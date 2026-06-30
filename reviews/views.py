from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework import viewsets, permissions, status, serializers
from rest_framework.response import Response

from products.models import Product
from .models import Review
from .forms import ReviewForm
from .serializers import ReviewSerializer

@login_required
def add_review_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        # Check if already reviewed
        existing_review = Review.objects.filter(user=request.user, product=product).first()
        
        if existing_review:
            form = ReviewForm(request.POST, instance=existing_review)
        else:
            form = ReviewForm(request.POST)
            
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()
            messages.success(request, "Your review has been submitted.")
        else:
            messages.error(request, "Failed to submit review. Check rating value.")
            
    return redirect('products:detail', slug=product.slug)

@login_required
def delete_review_view(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    product_slug = review.product.slug
    review.delete()
    messages.success(request, "Review deleted.")
    return redirect('products:detail', slug=product_slug)


# DRF Serializers & ViewSet
class DRFReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        product_id = self.request.data.get('product')
        product = get_object_or_404(Product, id=product_id)
        # Check if already reviewed
        if Review.objects.filter(user=self.request.user, product=product).exists():
            raise serializers.ValidationError("You have already reviewed this product.")
        serializer.save(user=self.request.user, product=product)

    def perform_update(self, serializer):
        review = self.get_object()
        if review.user != self.request.user:
            raise permissions.PermissionDenied("You cannot edit this review.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise permissions.PermissionDenied("You cannot delete this review.")
        instance.delete()
