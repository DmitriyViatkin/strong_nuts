
from wagtail.fields import   StreamField
from wagtail.admin.panels import FieldPanel
from wagtail.models import Page

from wagtail_cms.blocks import VideoBannerBlock, BenefitItemBlock, GalleryBlock


class GalleryPage(Page):

    template = 'cms_pages/gallery.html'
    max_count = 1

    top_banner = StreamField([
        ('video_banner', VideoBannerBlock()),
    ], blank=True, use_json_field=True, verbose_name='Банер', default=list)

    images = StreamField([
        ('item', GalleryBlock()),
    ], blank=True, use_json_field=True, verbose_name='Галерея')

    content_panels = Page.content_panels + [
        FieldPanel('top_banner'),
        FieldPanel('images'),
    ]

    class Meta:
        verbose_name = 'Галерея'