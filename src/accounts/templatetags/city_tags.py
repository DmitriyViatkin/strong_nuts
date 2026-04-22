from django import template
from django.utils.translation import get_language

register = template.Library()


def get_name_by_lang(obj, lang):
    if not obj.alternate_names:
        return obj.name

    names = [n.strip() for n in obj.alternate_names.split(';') if n.strip()]
    cyrillic = [n for n in names if any('\u0400' <= c <= '\u04FF' for c in n)]
    latin = [n for n in names if all(c.isascii() for c in n if c.isalpha())]

    if lang == 'uk':
        return cyrillic[-1] if cyrillic else obj.name
    elif lang == 'ru':
        return cyrillic[0] if cyrillic else obj.name
    elif lang == 'en':
        return latin[0] if latin else obj.name

    return obj.name


@register.filter
def localized_name(obj):
    lang = get_language() or 'uk'
    return get_name_by_lang(obj, lang)
