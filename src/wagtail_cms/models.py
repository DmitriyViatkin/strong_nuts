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
class BrandSettings(BaseSiteSetting):

    logo = models.ForeignKey('wagtailimages.Image', null=True, blank=True,
                             on_delete=models.SET_NULL, related_name='+', verbose_name=_('Логотип'))
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

    panels = [
        FieldPanel('logo'),
        FieldPanel('social_links'),
        FieldPanel('messenger_links'),
    ]

    class Meta:
        verbose_name = _('Налаштування бренду')


@register_setting
class NavLinks (BaseSiteSetting):

    naw_link = StreamField([('nav', NavLinkBlock())], use_json_field=True, blank=True,
                            verbose_name=_('Навігаційне меню')
                            )

    panels = [
        FieldPanel('naw_link'),
    ]


@register_setting
class HeaderSettings(BaseSiteSetting):


    top_banner_discount = models.CharField(
        max_length=200, blank=True,
        verbose_name=_('Текст банера знижки')
    )

    phone_numbers = StreamField(
        [('phone', PhoneBlock())],
        use_json_field=True, blank=True,
        verbose_name=_('Телефони')
    )

    button_text = models.CharField(
        max_length=50, blank=True,
        verbose_name=_('Текст кнопки')
    )
    text = models.CharField(
        max_length=250, blank=True,
        verbose_name=_('Текст')
    )
    button_working_hours = models.CharField(
        max_length=100, blank=True,
        verbose_name=_('Години роботи')
    )

    cart_icon = models.BooleanField(
        default=True,
        verbose_name=_('Показувати іконку кошика')
    )


    panels = [

        FieldPanel('top_banner_discount'),
        FieldPanel('phone_numbers'),
        FieldPanel('text'),
        FieldPanel('button_text'),
        FieldPanel('button_working_hours'),
        FieldPanel('cart_icon'),


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

    email = models.EmailField(
        blank=True,
        verbose_name=_('Email')
    )
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6,
        null=True, blank=True,
        verbose_name=_('Широта (Latitude)')
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6,
        null=True, blank=True,
        verbose_name=_('Долгота (Longitude)')
    )
    address = StreamField(
        [('address', AddressBlock())],
        use_json_field=True, blank=True,
        verbose_name=_('Адреси')
    )

    panels = [
        FieldPanel('seo'),
        FieldPanel('phone_numbers'),

        FieldPanel('email'),
        MultiFieldPanel([
            FieldPanel('latitude'),
            FieldPanel('longitude'),],heading=_("Координаты карты")),
        FieldPanel('address'),
    ]

    class Meta:
        verbose_name = _('Контактні дані')


@register_setting
class FooterSettings(BaseSiteSetting):


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