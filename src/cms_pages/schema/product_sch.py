from ninja import   Schema
from typing import List

class ProductSchema(Schema):
    id: int
    name: str
    summary: str = ''
    description: str
    mass: str = ''
    articul: str = ''
    packaging: str
    price: float
    is_active: bool
    image: List[str] = []

    @staticmethod
    def resolve_image(obj):
        return [
            img.image.url
            for img in obj.gallery.all()
            if img.image
        ]