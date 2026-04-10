from wagtail_modeltranslation.translation import TranslationOptions, register
from .models import (
    AboutManufacturerPage,
    AddressPage,
    CatalogProduct,
    CorporateClientsPage,
)
from .models import (
    DeliveryPaymentPage,
    HomePage,
    Main,
    Page404,
    NewsListPage,
    DetailNewsPage,
    GalleryPage,
    OrderPlaced,
    UserAgreement,
)



@register(AboutManufacturerPage)
class AboutManufacturerPageTranslationOptions(TranslationOptions):
    fields = (
        'gallery_section_title',
        'news_section_title',
        'news_section_subtitle',
        'content',
        'top_baner',
        'image_baner',
    )

@register(AddressPage)
class AddressPageTranslationOptions(TranslationOptions):
    fields = (
        # Тут лише поле image, перекладати не потрібно
    )

@register(CatalogProduct)
class CatalogProductTranslationOptions(TranslationOptions):
    fields = (
        'image_top_baner',
        'content_block',
    )

@register(CorporateClientsPage)
class CorporateClientsPageTranslationOptions(TranslationOptions):
    fields = (
        'body_text',
        'image_top_banner',
        'content_block',
        'image_footer_banner',
    )



@register(DeliveryPaymentPage)
class DeliveryPaymentPageTranslationOptions(TranslationOptions):
    fields = (
        'image_top_banner',
        'content_block',
        'video_footer_banner',
    )


@register(HomePage)
class HomePageTranslationOptions(TranslationOptions):
    fields = (
        # HomePage не має власних текстових полів
    )


@register(Main)
class MainTranslationOptions(TranslationOptions):
    fields = (
        'video_banner_url',
        'video_banner_title',
        'video_banner_text',
        'about_title',
        'about_text',
        'about_button_text',
        'about_button_url',
        'about_images',
        'promo_video_url',
        'promo_video_title',
        'promo_video_text',
        'benefit_title',
        'benefit_subtitle',
        'benefit_items',
        'eco_title',
        'eco_text',
        'eco_url',
        'news_title',
        'news_subtitle',
    )


@register(Page404)
class Page404TranslationOptions(TranslationOptions):
    fields = (
        'text',
    )


@register(NewsListPage)
class NewsListPageTranslationOptions(TranslationOptions):
    fields = (
        'title_page',
        'subtitle',
        'promo_banner',
    )


@register(DetailNewsPage)
class DetailNewsPageTranslationOptions(TranslationOptions):
    fields = (
        'title_page',
        'body',
    )


@register(GalleryPage)
class GalleryPageTranslationOptions(TranslationOptions):
    fields = (
        'top_banner',
        'images',
    )


@register(OrderPlaced)
class OrderPlacedTranslationOptions(TranslationOptions):
    fields = (
        'thanks_title',
        'banner_title',
        'image_banner',
    )


@register(UserAgreement)
class UserAgreementTranslationOptions(TranslationOptions):
    fields = (
        'text',
    )