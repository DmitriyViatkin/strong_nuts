from django.db import models
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.models import Image
from wagtail.models import Page
from wagtail.blocks import RichTextBlock
from wagtail_cms.blocks import VideoBannerBlock, BenefitItemBlock, GalleryBlock
from cms_pages.models.about import AboutManufacturerPage
from product_management.models import Product
from .detail_news_page import DetailNewsPage

class HomePage(Page):
    template = 'cms_pages/main/index.html'
    max_count = 1

    # Відео банер (Топ)
    top_banner = StreamField([
        ('video_banner', VideoBannerBlock()),
    ], blank=True, use_json_field=True, verbose_name='Топ банер', max_num=1)

    # Секція "Про виробника" на головній
    about_title = models.CharField(max_length=255, blank=True, verbose_name="Заголовок (якщо пустий - візьме зі сторінки)")
    about_text = RichTextField(blank=True, verbose_name="Короткий опис для головної")
    about_button_text = models.CharField(max_length=100, blank=True, default="Читати більше")
    about_images = StreamField([
        ('image', ImageChooserBlock(label='Зображення')),
    ], blank=True, use_json_field=True)

    # Промо відео
    promo_video_section = StreamField([
        ('video_banner', VideoBannerBlock()),
    ], blank=True, use_json_field=True, verbose_name='Промо відео секція', max_num=1)

    # Про користь продукту
    benefit_title = models.CharField(max_length=255, blank=True)
    benefit_subtitle = models.CharField(max_length=255, blank=True)
    benefit_items = StreamField([
        ('item', BenefitItemBlock()),
    ], blank=True, use_json_field=True)

    # Еко банер
    eco_banner_section = StreamField([
        ('video_banner', VideoBannerBlock()),
    ], blank=True, use_json_field=True, verbose_name='Еко банер секція', max_num=1)

    # Новини
    news_title = models.CharField(max_length=255, blank=True)
    news_subtitle = models.CharField(max_length=255, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('top_banner'),
        MultiFieldPanel([
            FieldPanel('about_title'),
            FieldPanel('about_text'),
            FieldPanel('about_button_text'),
            FieldPanel('about_images'),
        ], heading='Секція: Про виробника'),
        FieldPanel('promo_video_section'),
        MultiFieldPanel([
            FieldPanel('benefit_title'),
            FieldPanel('benefit_subtitle'),
            FieldPanel('benefit_items'),
        ], heading='Секція: Про користь продукту'),
        FieldPanel('eco_banner_section'),
        MultiFieldPanel([
            FieldPanel('news_title'),
            FieldPanel('news_subtitle'),
        ], heading='Секція: Новини'),
    ]

    def get_context(self, request):
        context = super().get_context(request)


        context['news'] = DetailNewsPage.objects.live().order_by('-date')[:6]
        context['products'] = Product.objects.filter(is_active=True).order_by('-created_at')[:6]

        about_page = AboutManufacturerPage.objects.live().first()

        if about_page:
            context['about_manufacturer'] = about_page
            context['about_page_url'] = about_page.url

            context['about_remote_content'] = about_page.content

        return context

    class Meta:
        verbose_name = 'Головна сторінка'

    subpage_types = [
        'cms_pages.NewsListPage',
        'cms_pages.GalleryPage',
        'cms_pages.Page404',
        'cms_pages.AboutManufacturerPage',
        'cms_pages.OrderPlaced',
        'cms_pages.CorporateClientsPage',
        'cms_pages.DeliveryPaymentPage',
        'cms_pages.UserAgreement',
        'cms_pages.CatalogProduct',
        'cms_pages.AddressPage',
        'cms_pages.DetailNewsPage',
    ]


"""
class Main(Page):

    template = 'cms_pages/main/index.html'
    max_count = 1

    # Відео банер
    top_banner = StreamField([
        ('video_banner', VideoBannerBlock()),
    ], blank=True, use_json_field=True, verbose_name='Банер', default=list)

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
        FieldPanel('top_banner'),

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
        """


class Page404(Page):

    template = "cms_pages/404.html"
    max_count = 1

    image = models.ImageField(upload_to="404/", null=True, blank=True)
    text = models.CharField(max_length=255, blank=True)

    content_panels = Page.content_panels + [
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
        ('video_banner', VideoBannerBlock()),
    ], blank=True, use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel('title_page'),
        FieldPanel('subtitle'),
        FieldPanel('promo_banner'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        news = DetailNewsPage.objects.live().order_by('-date')
        context['first_news'] = news.first()
        context['other_news'] = news[1:4]
        return context

    class Meta:
        verbose_name = "Сторінка новин"





