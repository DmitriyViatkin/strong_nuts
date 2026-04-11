from wagtail_modeltranslation.translation import TranslationOptions, register
from .models import Gallery, Product



@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = (
        'name',
        'summary',
        'description',

        'composition',

        'storage_conditions',

    )
