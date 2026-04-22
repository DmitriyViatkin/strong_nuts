from django.db import models
from wagtail.fields import   StreamField
from wagtail.admin.panels import FieldPanel
from wagtail.images.blocks import ImageChooserBlock

from wagtail.models import Page
from wagtail.blocks import RichTextBlock




class DetailNewsPage(Page):



    template = "cms_pages/news/one-new.html"
    parent_page_types = ['cms_pages.NewsListPage']

    title_page = models.CharField(max_length=255, blank=True)
    date = models.DateField()
    body = StreamField([
        ('text', RichTextBlock(label="Текст")),
        ('image', ImageChooserBlock(label="Зображення")),
    ], blank=True, use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel('title_page'),
        FieldPanel('date'),
        FieldPanel('body'),
    ]

    def get_first_image(self):
        for block in self.body:
            if block.block_type == 'image':
                return block.value
        return None

    def get_context(self, request):
        context = super().get_context(request)
        context['latest_news'] = DetailNewsPage.objects.live().exclude(
            pk=self.pk
        ).order_by('-date')[:3]
        return context

    class Meta:
        verbose_name = "Новина"