from ninja import Router
from ..models import Product

router = Router()
@router.get("/")
def list_flavors(request):
    flavors = Product.objects.values_list("flavor_categories", flat=True).distinct()
    return {"flavors": list(flavors)}