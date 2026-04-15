from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.OrderCreateView.as_view(), name='order_checkout'),
    path('order/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('orders/<int:pk>/repeat/', views.RepeatOrderView.as_view(), name='order-repeat'),


]