from wagtail_modeltranslation.translation import TranslationOptions, register
from .models import User, Address

@register(User)
class UserTranslationOptions(TranslationOptions):
    fields = (
        'first_name',
        'second_name',
        'last_name',
        'avatar',
    )

@register(Address)
class AddressTranslationOptions(TranslationOptions):
    fields = (
        'street',
        'house',
        'apartment',
        'city',
        'company_name',
    )
