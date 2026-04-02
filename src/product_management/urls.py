from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    path('product/<int:pk>/', views.ProductCartDetailView.as_view(), name='product_cart'),
]