from ninja import Router
from ..models import Product

router = Router()
@router.get("/products")
def list_products(request):
    products = Product.objects.all()
    return {"products": list(products.values('name'))}