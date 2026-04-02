from django.db import models
from wagtail.fields import StreamField, RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.models import Page
from wagtail.blocks import StructBlock, CharBlock, RichTextBlock, URLBlock
from wagtail.images.blocks import ImageChooserBlock

from .blocks import ContentBlock, BanerBlock
from product_management.models import Product
from wagtail_cms.blocks import (
    VideoBannerBlock,
    StatisticItemBlock,
    GalleryBlock,
)


class CatalogProduct(Page):
    template = 'cms_page/catalog_product.html'
    max_count = 1

    image_top_baner = StreamField(
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

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel('image_top_baner'),
                FieldPanel('content_block'),


            ]
        )
    ]
    def get_context(self, request):

        context = super().get_context(request)
        context['ware'] = Product.objects.all().order_by('-date')[:6]

        return context

    class Meta:
        verbose_name = 'Страница каталог продукции'
        verbose_name_plural = 'Страницы каталог продукции'