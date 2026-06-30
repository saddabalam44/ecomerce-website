from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q, Avg
from rest_framework import viewsets, permissions, filters as drf_filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import Category, Product, ProductImage, ProductVariant
from reviews.models import Review
from .serializers import CategorySerializer, ProductSerializer

def product_list_view(request):
    products = Product.objects.filter(is_active=True).annotate(avg_rating=Avg('reviews__rating'))
    categories = Category.objects.filter(parent=None)

    # Search filter
    query = request.GET.get('q')
    if query:
        products = products.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )

    # Category filter
    category_slug = request.GET.get('category')
    selected_category = None
    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        # Include products of subcategories too
        subcategory_ids = selected_category.children.values_list('id', flat=True)
        category_ids = [selected_category.id] + list(subcategory_ids)
        products = products.filter(category_id__in=category_ids)

    # Price filter
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    # Sorting
    sort_by = request.GET.get('sort')
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'rating':
        products = products.order_by('-avg_rating')
    else:  # default or 'latest'
        products = products.order_by('-created_at')

    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'products/product_list.html', {
        'page_obj': page_obj,
        'categories': categories,
        'selected_category': selected_category,
        'query': query,
        'min_price': min_price,
        'max_price': max_price,
        'sort_by': sort_by,
    })

def product_detail_view(request, slug):
    product = get_object_or_404(Product.objects.filter(is_active=True).annotate(avg_rating=Avg('reviews__rating')), slug=slug)
    reviews = product.reviews.all()
    variants = product.variants.all()
    
    # Calculate average rating and total counts
    avg_rating = product.avg_rating or 0.0
    
    # Check if current user has already reviewed the product
    user_review = None
    if request.user.is_authenticated:
        user_review = Review.objects.filter(user=request.user, product=product).first()

    return render(request, 'products/product_detail.html', {
        'product': product,
        'reviews': reviews,
        'variants': variants,
        'avg_rating': avg_rating,
        'user_review': user_review,
    })


# DRF REST API Views
class DRFCategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'

class DRFProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_active=True).annotate(avg_rating=Avg('reviews__rating'))
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend, drf_filters.SearchFilter, drf_filters.OrderingFilter]
    filterset_fields = ['category__slug', 'is_featured']
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at', 'avg_rating']
