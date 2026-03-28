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

from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail_cms.blocks import VideoBannerBlock, BenefitItemBlock, GalleryBlock

class HomePage(Page):
    max_count = 1
    def serve(self, request):
        from django.shortcuts import redirect
        main = self.get_children().live().first()
        if main:
            return redirect(main.url)
        return super().serve(request)

class Main (Page):

    template = 'cms_pages/main/index.html'
    max_count = 1

    # Видео баннер

    video_banner_url = models.URLField(blank=True)
    video_banner_title = models.CharField(max_length=255, blank=True)
    video_banner_text = models.CharField(max_length=255, blank=True)

    # О производителе
    about_title = models.CharField(max_length=255, blank=True)
    about_text = RichTextField(blank=True)
    about_button_text = models.CharField(max_length=100, blank=True)
    about_button_url = models.URLField(blank=True)
    about_images = StreamField([
        ('image', ImageChooserBlock(label='Зображення')),
    ], blank=True, use_json_field=True)

    # Промо видео

    promo_video_url = models.URLField(blank=True)
    promo_video_title = models.CharField(max_length=255, blank=True)
    promo_video_text = models.CharField(max_length=255, blank=True)

    # О пользе продукта
    benefit_title = models.CharField(max_length=255, blank=True)
    benefit_subtitle = models.CharField(max_length=255, blank=True)
    benefit_items = StreamField([
        ('item', BenefitItemBlock()),
    ], blank=True, use_json_field=True)

    # Эко баннер

    eco_title = models.CharField(max_length=255, blank=True)
    eco_text = models.CharField(max_length=255, blank=True)
    eco_url = models.URLField(blank=True)

    # Новости
    news_title = models.CharField(max_length=255, blank=True)
    news_subtitle = models.CharField(max_length=255, blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel([

            FieldPanel('video_banner_url'),
            FieldPanel('video_banner_title'),
            FieldPanel('video_banner_text'),
        ], heading='Відео банер'),

        MultiFieldPanel([
            FieldPanel('about_title'),
            FieldPanel('about_text'),
            FieldPanel('about_button_text'),
            FieldPanel('about_button_url'),
            FieldPanel('about_images'),
        ], heading='Про виробника'),

        MultiFieldPanel([

            FieldPanel('promo_video_url'),
            FieldPanel('promo_video_title'),
            FieldPanel('promo_video_text'),
        ], heading='Промо відео'),

        MultiFieldPanel([
            FieldPanel('benefit_title'),
            FieldPanel('benefit_subtitle'),
            FieldPanel('benefit_items'),
        ], heading='Про користь продукту'),

        MultiFieldPanel([

            FieldPanel('eco_title'),
            FieldPanel('eco_text'),
            FieldPanel('eco_url'),
        ], heading='Еко банер'),

        MultiFieldPanel([
            FieldPanel('news_title'),
            FieldPanel('news_subtitle'),
        ], heading='Новини'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context['news'] = DetailNewsPage.objects.live().order_by('-date')[:6]
        return context

    class Meta:
        verbose_name = 'Головна сторінка'

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




class GalleryPage(Page):

    template = 'cms_pages/gallery.html'
    max_count = 1

    top_banner = StreamField([
        ('video_banner', VideoBannerBlock()),
    ], blank=True, use_json_field=True, verbose_name='Банер', default=list,  )

    images = StreamField([
        ('item', GalleryBlock()),
    ], blank=True, use_json_field=True, verbose_name='Галерея')

    content_panels = Page.content_panels + [
        FieldPanel('top_banner'),
        FieldPanel('images'),
    ]

    class Meta:
        verbose_name = 'Галерея'