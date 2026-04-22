from django.db import models
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.models import Page
from wagtail.blocks import StructBlock, CharBlock, RichTextBlock, URLBlock
from wagtail.images.blocks import ImageChooserBlock
from .detail_news_page import DetailNewsPage
from .gallery_page import GalleryPage
from .blocks import ContentBlock, BanerBlock
from wagtail_cms.blocks import (
    VideoBannerBlock,
    StatisticItemBlock,
    GalleryBlock,
)

class OrderPlaced(Page):
    template = 'cms_pages/thanks.html'
    max_count = 1



    thanks_title = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Заголовок секции благодарности',
    )
    banner_title = models.CharField(

        max_length=255,
        blank=True,
        verbose_name='Текст секции благодарности',
    )
    image_banner = StreamField(
        [('image_baner', BanerBlock())],
        blank=True,
        use_json_field=True,
        verbose_name='Баннер с изображением',
    )
    content_panels = Page.content_panels+[
        MultiFieldPanel([
            FieldPanel('thanks_title'),
            FieldPanel('banner_title'),
            FieldPanel('image_banner'),
        ], heading='Секция благодарности')
    ]

    class Meta:
        verbose_name = 'Страница благодарности за заказ'
        verbose_name_plural = 'Страницы благодарности за заказ'