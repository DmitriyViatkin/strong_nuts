from wagtail_modeltranslation.translation import TranslationOptions, register
from .models import (
    BrandSettings, NavLinks, HeaderSettings,
    ContactSettings, FooterSettings, StatisticSettings
)


@register(BrandSettings)
class BrandSettingsTranslationOptions(TranslationOptions):
    fields = (
        'social_links',
        'messenger_links',
    )

@register(NavLinks)
class NavLinksTranslationOptions(TranslationOptions):
    fields = (
        'naw_link',
    )

@register(HeaderSettings)
class HeaderSettingsTranslationOptions(TranslationOptions):
    fields = (
        'top_banner_discount',
        'phone_number',
        'button_text',
        'button_working_hours',
    )

@register(ContactSettings)
class ContactSettingsTranslationOptions(TranslationOptions):
    fields = (
        'seo',
        'phone_numbers',
        'email',
        'map_embed_url',
        'address',
    )

@register(FooterSettings)
class FooterSettingsTranslationOptions(TranslationOptions):
    fields = (
        'developer_name',
        'developer_url',
        'copyright_text',
    )

@register(StatisticSettings)
class StatisticSettingsTranslationOptions(TranslationOptions):
    fields = (
        'items',
    )

