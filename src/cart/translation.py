from wagtail_modeltranslation.translation import TranslationOptions, register
from cabinet.models import User, Address
from cart.models import Cart, CartItem
from product_management.models import Product





@register(Cart)
class CartTranslationOptions(TranslationOptions):
    fields = (
        'session_key',
    )


