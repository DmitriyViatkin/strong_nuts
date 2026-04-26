from django import template
from django.utils.translation import get_language

register = template.Library()


def get_name_by_lang(obj, lang):
    if not obj.alternate_names:
        return obj.name

    names = [n.strip() for n in obj.alternate_names.split(';') if n.strip()]

    for name in names:
        low = name.lower()

        if lang == 'uk':
            if any(c in low for c in ['і', 'ї', 'є', 'ґ']):
                return name

        elif lang == 'ru':
            if any(c in low for c in ['ы', 'э', 'ё']):
                return name

        elif lang == 'en':
            if name.isascii():
                return name

    return obj.name


@register.filter
def localized_name(obj):
    lang = get_language() or 'uk'
    return get_name_by_lang(obj, lang)
