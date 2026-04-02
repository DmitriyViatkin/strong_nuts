from django.shortcuts import render
from .models import Product
from django.views.generic import DetailView

class ProductCartDetailView(DetailView):
    model = Product
    template_name = 'product.html'
    context_object_name = 'product'

    def get_queryset(self):
        # Предзагружаем картинки, чтобы избежать N+1 запросов при отображении галереи
        return super().get_queryset().prefetch_related('gallery')
