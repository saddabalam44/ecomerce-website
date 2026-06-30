from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('notification/dismiss/<int:pk>/', views.dismiss_notification_view, name='dismiss_notification'),
]
