


from django import template
from django.utils.translation import get_language

register = template.Library()

def is_cyrillic(name):
    return any('\u0400' <= c <= '\u04FF' for c in name)

def is_russian(name):
    return any(c in name for c in ['ы', 'э', 'ё', 'ъ', 'Ы', 'Э', 'Ё', 'Ъ'])

def is_ascii(name):
    return name.isascii()

def get_name_by_lang(obj, lang):
    if not obj.alternate_names:
        return obj.name

    names = [n.strip() for n in obj.alternate_names.split(';') if n.strip()]

    if lang == 'uk':
        # Кирилиця без російських літер = українська
        for name in names:
            if is_cyrillic(name) and not is_russian(name):
                return name

    elif lang == 'ru':
        for name in names:
            if is_cyrillic(name) and is_russian(name):
                return name

    elif lang == 'en':
        for name in names:
            if is_ascii(name):
                return name

    return obj.name

@register.filter
def localized_name(obj):
    lang = get_language() or 'uk'
    return get_name_by_lang(obj, lang)
