import os
from django.core.management.base import BaseCommand
from django.core.files.images import ImageFile
from wagtail.models import Page, Site
from wagtail.images.models import Image as WagtailImage

from wagtail_cms.models import (
    HeaderSettings, ContactSettings,
    FooterSettings, StatisticSettings,
)
from cms_pages.models import (
    Main, Page404, NewsListPage, GalleryPage
)
from cms_pages.models.about import AboutManufacturerPage
from cms_pages.models.catalog_products import CatalogProduct
from cms_pages.models.corporate_clients_page import CorporateClientsPage
from cms_pages.models.delivery_payment import DeliveryPaymentPage
from cms_pages.models.order_placed import OrderPlaced
from cms_pages.models.user_agreement import UserAgreement

from .fixtures.initial_data import (
    HEADER, CONTACTS, FOOTER, STATISTICS,
    MAIN_PAGE, MAIN_PAGE_IMAGES,
    PAGE_404, PAGE_404_IMAGE,
    ABOUT_PAGE, ABOUT_PAGE_IMAGES,
    CATALOG_PAGE_IMAGES,
    CORPORATE_PAGE, CORPORATE_PAGE_IMAGES,
    DELIVERY_PAGE_IMAGES,
    ORDER_PAGE, ORDER_PAGE_IMAGES,
    NEWS_LIST_PAGE, GALLERY_PAGE, USER_AGREEMENT_PAGE,
)


class Command(BaseCommand):
    help = 'Початкове наповнення CMS даними'

    def handle(self, *args, **options):
        site = Site.objects.filter(is_default_site=True).first()
        if not site:
            self.stdout.write(self.style.ERROR('Дефолтний сайт не знайдено'))
            return

        # BaseSiteSetting — один універсальний метод
        self._setup(site, HeaderSettings,    HEADER,      'HeaderSettings')
        self._setup(site, ContactSettings,   CONTACTS,    'ContactSettings')
        self._setup(site, FooterSettings,    FOOTER,      'FooterSettings')
        self._setup(site, StatisticSettings, STATISTICS,  'StatisticSettings')

        # Прості Page (без картинок)
        self._setup_page(NewsListPage,   'news',      'Новини',            NEWS_LIST_PAGE)
        self._setup_page(GalleryPage,    'gallery',   'Галерея',           GALLERY_PAGE)
        self._setup_page(UserAgreement,  'agreement', 'Користувацька угода', USER_AGREEMENT_PAGE)

        # Page з картинками — свій метод
        self._setup_main_page()
        self._setup_page_404()
        self._setup_about_page()
        self._setup_catalog_page()
        self._setup_corporate_page()
        self._setup_delivery_page()
        self._setup_order_page()

    # ------------------------------------------------------------------ #
    #  Хелпери                                                            #
    # ------------------------------------------------------------------ #

    def _is_empty(self, value):
        if value is None:
            return True
        if isinstance(value, str):
            return value.strip() == ''
        if isinstance(value, (list, dict)):
            return len(value) == 0
        return False

    def _get_root_page(self):
        return Page.objects.filter(depth=2).first()

    def _get_or_create_image(self, filename: str):
        """Повертає Wagtail-картинку, або завантажує з fixtures/images/"""
        title = os.path.splitext(filename)[0]

        existing = WagtailImage.objects.filter(title=title).first()
        if existing:
            return existing

        images_dir = os.path.join(os.path.dirname(__file__), 'fixtures', 'images')
        filepath = os.path.join(images_dir, filename)

        if not os.path.exists(filepath):
            self.stdout.write(self.style.WARNING(f'  Файл не знайдено: {filepath}'))
            return None

        with open(filepath, 'rb') as f:
            image = WagtailImage(title=title)
            image.file.save(filename, ImageFile(f), save=True)
            self.stdout.write(self.style.SUCCESS(f'  Картинку завантажено: {filename}'))
            return image

    def _build_baner_stream(self, blocks_data: list) -> list:
        """
        Збирає StreamField для BanerBlock.
        Кожен елемент blocks_data — dict з ключами:
          block_type, image (filename), title, text, button_text, button_url
        """
        result = []
        for item in blocks_data:
            img = self._get_or_create_image(item['image'])
            if not img:
                continue
            result.append((
                item['block_type'],
                {
                    'image':       img.pk,
                    'title':       item.get('title', ''),
                    'text':        item.get('text', ''),
                    'button_text': item.get('button_text', ''),
                    'button_url':  item.get('button_url', ''),
                }
            ))
        return result

    def _build_content_stream(self, blocks_data: list) -> list:
        """
        Збирає StreamField для ContentBlock.
        Кожен елемент blocks_data — dict з ключами:
          block_type, image (filename), title, body_text, button_text, button_url
        """
        result = []
        for item in blocks_data:
            img = self._get_or_create_image(item['image'])
            if not img:
                continue
            result.append((
                item['block_type'],
                {
                    'image':       img.pk,
                    'title':       item.get('title', ''),
                    'body_text':   item.get('body_text', ''),
                    'button_text': item.get('button_text', ''),
                    'button_url':  item.get('button_url', ''),
                }
            ))
        return result

    def _save_page(self, page, label: str, changed: bool):
        if changed:
            page.save_revision().publish()
            self.stdout.write(self.style.SUCCESS(f'{label} успішно оновлено'))
        else:
            self.stdout.write(self.style.WARNING(f'{label} вже заповнена — пропущено'))

    # ------------------------------------------------------------------ #
    #  BaseSiteSetting — універсальний метод                              #
    # ------------------------------------------------------------------ #

    def _setup(self, site, model, data: dict, label: str):
        instance = model.for_site(site)
        changed = False
        for field, value in data.items():
            if self._is_empty(getattr(instance, field, None)):
                setattr(instance, field, value)
                changed = True
        if changed:
            instance.save()
            self.stdout.write(self.style.SUCCESS(f'{label} успішно оновлено'))
        else:
            self.stdout.write(self.style.WARNING(f'{label} вже заповнені — пропущено'))

    # ------------------------------------------------------------------ #
    #  Page — базовий метод для простих сторінок                          #
    # ------------------------------------------------------------------ #

    def _setup_page(self, model, slug: str, title: str, data: dict):
        label = model.__name__
        page = model.objects.first()

        if not page:
            parent = self._get_root_page()
            if not parent:
                self.stdout.write(self.style.ERROR(f'{label}: батьківська сторінка не знайдена'))
                return
            page = model(title=title, slug=slug)
            parent.add_child(instance=page)

        changed = False
        for field, value in data.items():
            if self._is_empty(getattr(page, field, None)):
                setattr(page, field, value)
                changed = True

        self._save_page(page, label, changed)

    # ------------------------------------------------------------------ #
    #  Page — методи для сторінок з картинками                            #
    # ------------------------------------------------------------------ #

    def _setup_main_page(self):
        label = 'Main'
        page = Main.objects.first()
        if not page:
            page = Main(title='Головна сторінка', slug='main')
            self._get_root_page().add_child(instance=page)

        changed = False

        for field, value in MAIN_PAGE.items():
            if self._is_empty(getattr(page, field, None)):
                setattr(page, field, value)
                changed = True

        # about_images — StreamField[ImageChooserBlock]
        if self._is_empty(page.about_images):
            images = []
            for filename in MAIN_PAGE_IMAGES.get('about_images', []):
                img = self._get_or_create_image(filename)
                if img:
                    images.append(('image', img.pk))
            if images:
                page.about_images = images
                changed = True

        self._save_page(page, label, changed)

    def _setup_page_404(self):
        label = 'Page404'
        page = Page404.objects.first()
        if not page:
            page = Page404(title='404', slug='404')
            self._get_root_page().add_child(instance=page)

        changed = False

        for field, value in PAGE_404.items():
            if self._is_empty(getattr(page, field, None)):
                setattr(page, field, value)
                changed = True

        if not page.image:
            img = self._get_or_create_image(PAGE_404_IMAGE)
            if img:
                page.image = img.file.name
                changed = True

        self._save_page(page, label, changed)

    def _setup_about_page(self):
        label = 'AboutManufacturerPage'
        page = AboutManufacturerPage.objects.first()
        if not page:
            page = AboutManufacturerPage(title='Про виробника', slug='about')
            self._get_root_page().add_child(instance=page)

        changed = False

        # Текстові поля
        for field, value in ABOUT_PAGE.items():
            if self._is_empty(getattr(page, field, None)):
                setattr(page, field, value)
                changed = True

        # content — StreamField[ContentBlock]
        if self._is_empty(page.content):
            stream = self._build_content_stream(ABOUT_PAGE_IMAGES.get('content', []))
            if stream:
                page.content = stream
                changed = True

        # image_baner — StreamField[BanerBlock]
        if self._is_empty(page.image_baner):
            stream = self._build_baner_stream(ABOUT_PAGE_IMAGES.get('image_baner', []))
            if stream:
                page.image_baner = stream
                changed = True

        self._save_page(page, label, changed)

    def _setup_catalog_page(self):
        label = 'CatalogProduct'
        page = CatalogProduct.objects.first()
        if not page:
            page = CatalogProduct(title='Каталог', slug='catalog')
            self._get_root_page().add_child(instance=page)

        changed = False

        if self._is_empty(page.image_top_baner):
            stream = self._build_baner_stream(CATALOG_PAGE_IMAGES.get('image_top_baner', []))
            if stream:
                page.image_top_baner = stream
                changed = True

        if self._is_empty(page.content_block):
            stream = self._build_content_stream(CATALOG_PAGE_IMAGES.get('content_block', []))
            if stream:
                page.content_block = stream
                changed = True

        self._save_page(page, label, changed)

    def _setup_corporate_page(self):
        label = 'CorporateClientsPage'
        page = CorporateClientsPage.objects.first()
        if not page:
            page = CorporateClientsPage(title='Корпоративним клієнтам', slug='corporate')
            self._get_root_page().add_child(instance=page)

        changed = False

        for field, value in CORPORATE_PAGE.items():
            if self._is_empty(getattr(page, field, None)):
                setattr(page, field, value)
                changed = True

        if self._is_empty(page.image_top_banner):
            stream = self._build_baner_stream(CORPORATE_PAGE_IMAGES.get('image_top_banner', []))
            if stream:
                page.image_top_banner = stream
                changed = True

        if self._is_empty(page.image_footer_banner):
            stream = self._build_baner_stream(CORPORATE_PAGE_IMAGES.get('image_footer_banner', []))
            if stream:
                page.image_footer_banner = stream
                changed = True

        if self._is_empty(page.content_block):
            stream = self._build_content_stream(CORPORATE_PAGE_IMAGES.get('content_block', []))
            if stream:
                page.content_block = stream
                changed = True

        self._save_page(page, label, changed)

    def _setup_delivery_page(self):
        label = 'DeliveryPaymentPage'
        page = DeliveryPaymentPage.objects.first()
        if not page:
            page = DeliveryPaymentPage(title='Доставка і оплата', slug='delivery')
            self._get_root_page().add_child(instance=page)

        changed = False

        if self._is_empty(page.image_top_banner):
            stream = self._build_baner_stream(DELIVERY_PAGE_IMAGES.get('image_top_banner', []))
            if stream:
                page.image_top_banner = stream
                changed = True

        if self._is_empty(page.content_block):
            stream = self._build_content_stream(DELIVERY_PAGE_IMAGES.get('content_block', []))
            if stream:
                page.content_block = stream
                changed = True

        self._save_page(page, label, changed)

    def _setup_order_page(self):
        label = 'OrderPlaced'
        page = OrderPlaced.objects.first()
        if not page:
            page = OrderPlaced(title='Дякуємо за замовлення', slug='order-placed')
            self._get_root_page().add_child(instance=page)

        changed = False

        for field, value in ORDER_PAGE.items():
            if self._is_empty(getattr(page, field, None)):
                setattr(page, field, value)
                changed = True

        if self._is_empty(page.image_banner):
            stream = self._build_baner_stream(ORDER_PAGE_IMAGES.get('image_banner', []))
            if stream:
                page.image_banner = stream
                changed = True

        self._save_page(page, label, changed)
