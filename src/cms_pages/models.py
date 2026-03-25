from django.db import models
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel
from wagtail_cms.blocks import VideoBannerBlock
from wagtail.images.models import Image
from wagtail.models import Page

from wagtail_cms.blocks import VideoBannerBlock


class HomePage(Page):
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

    template = 'cms_pages/news_list.html'

    title_page = RichTextField(blank=True)
    subtitle = RichTextField(blank=True)
    promo_banner = StreamField([
        ('video_banner', VideoBannerBlock()),], blank=True, use_json_field=True)
    content_panels =  Page.content_panels + [

        FieldPanel('title_page'),
        FieldPanel('subtitle'),
        FieldPanel('promo_banner'),

    ]

class DetailNewsPage(Page):

    template = "news/one-new.html"

    title_page= models.CharField(max_length = 255)
    date = models.DateField()
    text = RichTextField(blank= True)
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    content_panels = Page.content_panels + [
    FieldPanel('title_page'),
    FieldPanel('date'),
    FieldPanel('image'),
    FieldPanel('text'),

]

    def get_context(self, request):
        context = super().get_context(request)
        context['news'] = DetailNewsPage.objects.live().order_by('-date')
        return context

class Meta:
    verbose_name = "Новина"
