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

    Page404,
    NewsListPage,
    DetailNewsPage,
    GalleryPage,
    OrderPlaced,
    UserAgreement,


)

@register(AddressPage)
class AddressPageTR(TranslationOptions):
    pass

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
class MainTranslationOptions(TranslationOptions):
    fields = (
        'top_banner',           # StreamField
        'about_title',
        'about_text',
        'about_button_text',
        'about_images',         # StreamField
        'promo_video_section',  # НОВА НАЗВА замість promo_video_text/title
        'benefit_title',
        'benefit_subtitle',
        'benefit_items',        # StreamField
        'eco_banner_section',   # НОВА НАЗВА замість eco_title/text
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