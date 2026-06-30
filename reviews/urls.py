from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('add/<int:product_id>/', views.add_review_view, name='add_review'),
    path('delete/<int:review_id>/', views.delete_review_view, name='delete_review'),
]
