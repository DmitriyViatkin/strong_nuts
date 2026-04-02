from ninja import NinjaAPI
from typing import List
from .schema.product_sch import  ProductSchema

from product_management.models import Product

api = NinjaAPI()

@api.get('/products', response = List[ProductSchema])
def get_products(request, page: int=1, per_page: int=6):
    offset = (page - 1) * per_page
    return (
        Product.objects.filter(is_active=True)
        .prefetch_related('gallery').order_by('-category_at')[offset:offset + per_page]
    )

