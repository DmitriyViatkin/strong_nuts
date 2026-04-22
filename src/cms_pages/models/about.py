from django.db import models
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.models import Page
from wagtail.blocks import StructBlock, CharBlock, RichTextBlock, URLBlock
from wagtail.images.blocks import ImageChooserBlock
from .gallery_page import  GalleryPage
from .detail_news_page import DetailNewsPage
from .blocks import ContentBlock, BanerBlock
from wagtail_cms.blocks import (
    VideoBannerBlock,
    StatisticItemBlock,
    GalleryBlock,
)


class AboutManufacturerPage(Page):
    """
    content      → ContentBlock         (свой блок)
    top_baner    → VideoBannerBlock      (из wagtail_cms.blocks)
    statistic    → StatisticItemBlock    (из wagtail_cms.blocks)
    image_baner  → BanerBlock            (свой блок)

    galery и news — НЕ StreamField, подтягиваются через get_context
    из GalleryPage и DetailNewsPage
    """

    template = 'cms_pages/about.html'
    max_count = 1

    # ── Заголовки секций (редактируются в админке) ─────────────────────────────

    gallery_section_title = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Заголовок секции галереи',
    )
    news_section_title = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Заголовок секции новостей',
    )
    news_section_subtitle = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Подзаголовок секции новостей',
    )

    # ── StreamField-поля ───────────────────────────────────────────────────────

    # content → ContentBlock
    content = StreamField(
        [('content', ContentBlock())],
        blank=True,
        use_json_field=True,
        verbose_name='Контент',
    )

    # top_baner → VideoBannerBlock
    top_baner = StreamField(
        [('top_baner', VideoBannerBlock())],
        blank=True,
        use_json_field=True,
        verbose_name='Видео баннер',
    )




    # image_baner → BanerBlock
    image_baner = StreamField(
        [('image_baner', BanerBlock())],
        blank=True,
        use_json_field=True,
        verbose_name='Баннер с изображением',
    )

    # ── Панели админки ─────────────────────────────────────────────────────────

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [FieldPanel('content')],
            heading='Контент',
        ),
        MultiFieldPanel(
            [FieldPanel('top_baner')],
            heading='Видео баннер',
        ),

        MultiFieldPanel(
            [FieldPanel('image_baner')],
            heading='Баннер с изображением',
        ),

        MultiFieldPanel(
            [FieldPanel('gallery_section_title')],
            heading='Галерея (данные из GalleryPage)',
        ),

        MultiFieldPanel(
            [
                FieldPanel('news_section_title'),
                FieldPanel('news_section_subtitle'),
            ],
            heading='Новости (данные из DetailNewsPage)',
        ),
    ]

    def get_context(self, request):

        context = super().get_context(request)
        context['news'] = DetailNewsPage.objects.live().order_by('-date')[:6]
        gallery_page = GalleryPage.objects.live().first()
        context['gallery_page'] = gallery_page
        context['gallery'] = gallery_page.images if gallery_page else []
        return context

    class Meta:
        verbose_name = 'Страница о производителе'