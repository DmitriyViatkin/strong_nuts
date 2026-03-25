from django.db import models
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel
from wagtail_cms.blocks import VideoBannerBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.models import Image
from wagtail.models import Page
from wagtail.blocks import RichTextBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.blocks import StructBlock, CharBlock
from wagtail_cms.blocks import VideoBannerBlock


class HomePage(Page):
    max_count = 1
    pass

class Page404(Page):

    template = "cms_pages/404.html"
    max_count = 1

    image = models.ImageField(
        upload_to="404/",
        null=True,
        blank=True
    )
    text = models.CharField(max_length= 255, blank=True)

    content_panels =  Page.content_panels + [
        FieldPanel("image"),
        FieldPanel("text"),
    ]

    class Meta:

        verbose_name = "404 сторінка"

class NewsListPage(Page):

    template = 'cms_pages/news/news_list.html'
    max_count = 1

    title_page = RichTextField(blank=True)
    subtitle = RichTextField(blank=True)
    promo_banner = StreamField([
        ('video_banner', VideoBannerBlock()),], blank=True, use_json_field=True)
    content_panels =  Page.content_panels + [

        FieldPanel('title_page'),
        FieldPanel('subtitle'),
        FieldPanel('promo_banner'),

    ]

    def get_context(self, request):
        context = super().get_context(request)
        news = DetailNewsPage.objects.live().order_by('-date')
        context['first_news'] = news.first()  # большая новость слева
        context['other_news'] = news[1:4]  # 3 маленьких карточки
        return context

    class Meta:
        verbose_name = "Сторінка новин"

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
