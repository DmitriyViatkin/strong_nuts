from ninja import NinjaAPI
from .list_packaging import router as packaging_router
from .list_flavors import router as flavors_router
from  .product import router as product_router
api= NinjaAPI()

api.add_router("/mass/",packaging_router)
api.add_router("/flavors/",flavors_router)
api.add_router("/products/",product_router)

