from wagtail_modeltranslation.translation import TranslationOptions, register
from .models import (
    BrandSettings, NavLinks, HeaderSettings,
    ContactSettings, FooterSettings, StatisticSettings
)




@register(NavLinks)
class NavLinksTranslationOptions(TranslationOptions):
    fields = (
        'nav_link',
    )

@register(HeaderSettings)
class HeaderSettingsTranslationOptions(TranslationOptions):
    fields = (


        'button_text',
        'text'

    )

@register(ContactSettings)
class ContactSettingsTranslationOptions(TranslationOptions):
    fields = (
        'seo',


        'address',
    )

@register(FooterSettings)
class FooterSettingsTranslationOptions(TranslationOptions):
    fields = (
        'developer_name',

        'copyright_text',
    )

@register(StatisticSettings)
class StatisticSettingsTranslationOptions(TranslationOptions):
    fields = (
        'items',
    )

