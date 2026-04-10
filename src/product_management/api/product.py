from ninja import Router
from ..models import Product, PACKAGING_CHOICE, FLAVOR_CATEGORIES_CHOICE

router = Router()


@router.get("/")
def get_products(request, flavor: str = None, mass: int = None, order: str = None):
    products = Product.objects.prefetch_related('gallery').filter(is_active=True)

    if flavor:
        products = products.filter(flavor_categories=flavor)
    if mass:
        products = products.filter(mass=mass)

    if order == 'asc':
        products = products.order_by('price')
    elif order == 'desc':
        products = products.order_by('-price')

    packaging_dict = dict(PACKAGING_CHOICE)
    flavor_dict = dict(FLAVOR_CATEGORIES_CHOICE)

    result = []
    for p in products:
        result.append({
            "id": p.id,
            "name": p.name,
            "articul": p.articul,
            "summary": p.summary,
            "mass": p.mass,
            "packaging": packaging_dict.get(p.packaging, p.packaging),
            "flavor": flavor_dict.get(p.flavor_categories, p.flavor_categories),
            "price": str(p.price),
            "old_price": str(p.old_price) if p.old_price else None,
            "is_sale": p.is_sale,
            "images": [img.image.url for img in p.gallery.all() if img.image],
        })

    return {"products": result}