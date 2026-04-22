from django.db import models
from wagtail.fields import StreamField, RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.models import Page
from wagtail.blocks import StructBlock, CharBlock, RichTextBlock, URLBlock
from .detail_news_page import DetailNewsPage
from .gallery_page import GalleryPage
from .blocks import ContentBlock, BanerBlock
from wagtail_cms.blocks import (
    VideoBannerBlock,
    StatisticItemBlock,
    GalleryBlock,
)

class CorporateClientsPage(Page):
    template = 'cms_pages/customers.html'
    max_count = 1


    body_text = RichTextField(
        blank=True,
        verbose_name='Текст страницы',
    )

    image_top_banner = StreamField(
        [('image_baner', BanerBlock())],
        blank=True,
        use_json_field=True,
        verbose_name='Баннер с изображением',
    )
    content_block = StreamField(
        [('content_block', ContentBlock())],
        blank=True,
        use_json_field=True,
        verbose_name='Контент страницы',
    )
    image_footer_banner = StreamField(
        [('image_baner', BanerBlock())],
        blank=True,
        use_json_field=True,
        verbose_name='Баннер с изображением в футере',
    )



    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('body_text'),
        ], heading='Текст страницы'),
        MultiFieldPanel([
            FieldPanel('image_top_banner'),
        ], heading='Баннер с изображением вверху страницы'),
        MultiFieldPanel([
            FieldPanel('content_block'),
        ], heading='Контент страницы'),
        MultiFieldPanel([
            FieldPanel('image_footer_banner'),
        ], heading='Баннер с изображением внизу страницы'),
    ]

    class Meta:
        verbose_name = 'Страница для корпоративных клиентов'
        verbose_name_plural = 'Страницы для корпоративных клиентов'