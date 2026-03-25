from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import  StreamField
from .blocks import (
    MessengerBlock, NavLinkBlock, SocialLinkBlock,
    PhoneBlock, AddressBlock, StatisticItemBlock
)

@register_setting
class HeaderSettings(BaseSiteSetting):

    logo = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_('Логотип')
    )
    top_banner_discount = models.CharField(
        max_length=200, blank=True,
        verbose_name=_('Текст банера знижки')
    )
    social_links = StreamField(
        [('social', SocialLinkBlock())],
        use_json_field=True, blank=True,
        verbose_name=_('Соцмережі')
    )
    messenger_links = StreamField(
        [('messenger', MessengerBlock())],
        use_json_field=True, blank=True,
        verbose_name=_('Месенджери')
    )
    phone_number = models.CharField(
        max_length=20, blank=True,
        verbose_name=_('Телефон')
    )
    button_text = models.CharField(
        max_length=50, blank=True,
        verbose_name=_('Текст кнопки')
    )
    button_working_hours = models.CharField(
        max_length=100, blank=True,
        verbose_name=_('Години роботи')
    )
    nav_links = StreamField(
        [('nav', NavLinkBlock())],
        use_json_field=True, blank=True,
        verbose_name=_('Навігаційне меню')
    )
    cart_icon = models.BooleanField(
        default=True,
        verbose_name=_('Показувати іконку кошика')
    )


    panels = [
        FieldPanel('logo'),
        FieldPanel('top_banner_discount'),
        FieldPanel('phone_number'),
        FieldPanel('button_text'),
        FieldPanel('button_working_hours'),
        FieldPanel('cart_icon'),

        FieldPanel('social_links'),
        FieldPanel('messenger_links'),
        FieldPanel('nav_links'),
    ]

    class Meta:
        verbose_name = _('Налаштування шапки')


@register_setting
class ContactSettings(BaseSiteSetting):

    seo = models.CharField(
        max_length=200, blank=True,
        verbose_name=_('SEO')
    )
    phone_numbers = StreamField(
        [('phone', PhoneBlock())],
        use_json_field=True, blank=True,
        verbose_name=_('Телефони')
    )
    messenger_links = StreamField(
        [('messenger', MessengerBlock())],
        use_json_field=True, blank=True,
        verbose_name=_('Месенджери')
    )
    email = models.EmailField(
        blank=True,
        verbose_name=_('Email')
    )
    map_embed_url = models.URLField(
        blank=True,
        verbose_name=_('URL карти')
    )
    address = StreamField(
        [('address', AddressBlock())],
        use_json_field=True, blank=True,
        verbose_name=_('Адреси')
    )

    panels = [
        FieldPanel('seo'),
        FieldPanel('phone_numbers'),
        FieldPanel('messenger_links'),
        FieldPanel('email'),
        FieldPanel('map_embed_url'),
        FieldPanel('address'),
    ]

    class Meta:
        verbose_name = _('Контактні дані')


@register_setting
class FooterSettings(BaseSiteSetting):

    logo = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_('Логотип')
    )
    nav_links = StreamField(
        [('nav', NavLinkBlock())],
        use_json_field=True, blank=True,
        verbose_name=_('Навігаційне меню')
    )
    social_links = StreamField(
        [('social', SocialLinkBlock())],
        use_json_field=True, blank=True,
        verbose_name=_('Соцмережі')
    )
    developer_name = models.CharField(
        max_length=100, blank=True,
        verbose_name=_('Розробник')
    )
    developer_url = models.URLField(
        blank=True,
        verbose_name=_('URL розробника')
    )
    copyright_text = models.CharField(
        max_length=200, blank=True,
        verbose_name=_('Копірайт')
    )

    panels = [
        FieldPanel('logo'),
        FieldPanel('nav_links'),
        FieldPanel('social_links'),
        FieldPanel('developer_name'),
        FieldPanel('developer_url'),
        FieldPanel('copyright_text'),
    ]

    class Meta:
        verbose_name = _('Налаштування футера')

@register_setting
class StatisticSettings(BaseSiteSetting):

    items = StreamField([
        ('item', StatisticItemBlock()),
    ], blank=True, use_json_field=True, verbose_name='Статистика')

    panels = [
        FieldPanel('items'),
    ]

    class Meta:
        verbose_name = _('Статистика')