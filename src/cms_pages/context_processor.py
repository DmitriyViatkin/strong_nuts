from cms_pages.models import AddressPage
from django.utils import translation
import re
from django.conf import settings

def google_maps_api_key(request):
    return {
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY
    }

def cabinet_pages (request):
    try:

        address_page = AddressPage.objects.live().first()
    except Exception:
        address_page = None

    return {
        'address_page': address_page
    }

def translated_urls(request):
    translations = {}
    languages = ['uk', 'en', 'ru']

    # Wagtail передає сторінку через serve() — перевіряємо різні атрибути
    page = (
        getattr(request, 'wagtailpage', None) or
        getattr(request, '_wagtail_page', None) or
        getattr(request, 'page', None)
    )

    if page and hasattr(page, 'get_translation'):
        for lang_code in languages:
            try:
                translated_page = page.get_translation(lang_code)
                with translation.override(lang_code):
                    translations[lang_code] = translated_page.url
            except Exception:
                # fallback — замінюємо лише префікс
                translations[lang_code] = re.sub(
                    r'^/(uk|en|ru)/', f'/{lang_code}/', request.path
                )
    else:

        for lang_code in languages:
            translations[lang_code] = re.sub(
                r'^/(uk|en|ru)/', f'/{lang_code}/', request.path
            )

    return {'translated_urls': translations}