from ninja import Router
from ..models import Product
router = Router()
@router.get("")
def get_mass(request, flavor: str = None):
    products = Product.objects.filter(is_active=True)
    if flavor:
        products = products.filter(flavor_categories=flavor)
    mass_list = list(
        products.values_list('mass', flat=True)
        .distinct()
        .order_by('mass')
    )
    return {"mass": [m for m in mass_list if m]}