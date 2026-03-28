from django.db import models
from wagtail.fields import StreamField, RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.models import Page
from wagtail.blocks import StructBlock, CharBlock, RichTextBlock, URLBlock
from wagtail.images.blocks import ImageChooserBlock
from .models import DetailNewsPage, GalleryPage
from .blocks import ContentBlock, BanerBlock
from wagtail_cms.blocks import (
    VideoBannerBlock,
    StatisticItemBlock,
    GalleryBlock,
)

class DeliveryPaymentPage(Page):
    template = 'cms_pages/delivery_payment.html'
    max_count = 1

    image_top_banner = StreamField(
        [('image_baner', BanerBlock())],
        blank=True,
        use_json_field=True,
        verbose_name='Баннер с изображением вверху страницы',
    )


    content_block = StreamField(
        [('content_block', ContentBlock())],
        blank=True,
        use_json_field=True,
        verbose_name='Контент страницы',
    )

    video_footer_banner = StreamField(
        [('image_banner', VideoBannerBlock())],
        blank=True,
        use_json_field=True,
        verbose_name='Баннер с изображением в футере',
    )

    content_panels = Page.content_panels + [

        MultiFieldPanel([
            FieldPanel('image_top_banner'),
        ], heading='Баннер с изображением вверху страницы'),
        MultiFieldPanel([
            FieldPanel('content_block'),
        ], heading='Контент страницы'),
        MultiFieldPanel([
            FieldPanel('video_footer_banner'),
        ], heading='Баннер с видео внизу страницы'),
    ]

    class Meta:
        verbose_name = 'Страница "Доставка и оплата"'
        verbose_name_plural = 'Страница "Доставка и оплата"'