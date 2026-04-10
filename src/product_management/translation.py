from wagtail_modeltranslation.translation import TranslationOptions, register
from .models import Gallery, Product

@register(Gallery)
class GalleryTranslationOptions(TranslationOptions):
    fields = (
        # Для Gallery перекладати можна лише поле image,
        # якщо ви хочете різні зображення для різних мов.
        'image',
    )

@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = (
        'name',
        'summary',
        'description',
        'mass',
        'composition',
        'energy_value',
        'storage_conditions',
        'articul',
    )
