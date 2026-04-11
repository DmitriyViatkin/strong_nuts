from django.shortcuts import render
from .models import Product
from django.views.generic import DetailView

class ProductCartDetailView(DetailView):
    model = Product
    template_name = 'product_management/product.html'
    context_object_name = 'product'

    def get_queryset(self):

        return super().get_queryset().prefetch_related('gallery')
