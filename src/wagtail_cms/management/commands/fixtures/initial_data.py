HEADER = {
    'top_banner_discount': 'Знижка 20% на всі послуги!',
    'phone_number': '+380123456789',
    'button_text': "Зв'язатись з нами",
    'button_working_hours': 'Пн-Пт: 9:00 - 18:00',
    'cart_icon': True,
}

CONTACTS = {
    'email': 'info@example.com',
    'map_embed_url': (
        'https://www.google.com/maps/embed?pb=!1m18...'
    ),
    'phone_numbers': [
        ('phone', {'number_1': '+380123456789', 'number_2': '+380987654321'}),
    ],
    'address': [
        ('address', {'name': 'Офіс у місті Київ', 'address': 'вул. Хрещатик, 123'}),
        ('address', {'name': 'Представництво',    'address': 'вул. Незалежності, 456'}),
    ],
}

FOOTER = {
    'developer_name': 'ТОВ "Розробники"',
    'developer_url': 'https://www.developer.com',
    'copyright_text': '© 2024 Всі права захищені.',
}

STATISTICS = {
    'items': [
        ('item', {'number': '240', 'unit': 'км',
                  'description': 'Траси',              'sub_description': ''}),
        ('item', {'number': '1',   'unit': 'км',
                  'description': 'Підйомник',          'sub_description': ''}),
        ('item', {'number': '10',  'unit': 'км',
                  'description': 'Довжина маршруту',   'sub_description': ''}),
        ('item', {'number': '80',  'unit': '%',
                  'description': 'Задоволених клієнтів','sub_description': ''}),
    ]
}


MAIN_PAGE = {
    'video_banner_url':   'https://example.com/video.mp4',
    'video_banner_title': 'Заголовок баннера',
    'video_banner_text':  'Текст баннера',
    'about_title':        'Про нас',
    'about_text':         '<p>Текст про компанію</p>',
    'about_button_text':  'Дізнатись більше',
    'about_button_url':   'https://example.com/promo.mp4',
    'promo_video_url':    'https://example.com/promo.mp4',
    'promo_video_title':  'Заголовок промо',
    'promo_video_text':   'Текст промо',
    'benefit_title':      'Наші переваги',
    'benefit_subtitle':   'Підзаголовок',
    'eco_title':          'Еко заголовок',
    'eco_text':           'Еко текст',
    'eco_url':            '/eco/',
    'news_title':         'Новини',
    'news_subtitle':      'Останні новини',
}

# StreamField з ImageChooserBlock — { назва_поля: [список файлів] }
MAIN_PAGE_IMAGES = {
    'about_images': ['about_1.jpg', 'about_2.jpg'],
}

PAGE_404 = {
    'text': 'Сторінку не знайдено. Поверніться на головну.',
}
PAGE_404_IMAGE = '404.png'  # models.ImageField

NEWS_LIST_PAGE = {
    'title_page': '<p>Новини</p>',
    'subtitle':   '<p>Останні події</p>',
}

GALLERY_PAGE = {

}
# ── AboutManufacturerPage ───────────────────────────────────────────────
ABOUT_PAGE = {
    'gallery_section_title': 'Наша галерея',
    'news_section_title':    'Новини',
    'news_section_subtitle': 'Останні події компанії',
}
ABOUT_PAGE_IMAGES = {
    'content': [
        {
            'block_type': 'content',
            'image':       'about_content.jpg',
            'title':       'Про виробника',
            'body_text':   '<p>Текст про виробника</p>',
            'button_text': 'Дізнатись більше',
            'button_url':  'http://127.0.0.1:8000/admin/',
        }
    ],
    'image_baner': [
        {
            'block_type':  'image_baner',
            'image':       'about_banner.jpg',
            'title':       'Заголовок банера',
            'text':        'Текст банера',
            'button_text': 'Перейти',
            'button_url':  'http://127.0.0.1:8000/admin/',
        }
    ],
}

# ── CatalogProduct ──────────────────────────────────────────────────────
CATALOG_PAGE_IMAGES = {
    'image_top_baner': [
        {
            'block_type':  'image_baner',
            'image':       'catalog_banner.jpg',
            'title':       'Каталог продукції',
            'text':        'Текст банера каталогу',
            'button_text': '',
            'button_url':  '',
        }
    ],
    'content_block': [
        {
            'block_type':  'content_block',
            'image':       'catalog_content.jpg',
            'title':       'Наша продукція',
            'body_text':   '<p>Опис продукції</p>',
            'button_text': 'Переглянути',
            'button_url':  'None',
        }
    ],
}

# ── CorporateClientsPage ────────────────────────────────────────────────
CORPORATE_PAGE = {
    'body_text': '<p>Текст для корпоративних клієнтів</p>',
}
CORPORATE_PAGE_IMAGES = {
    'image_top_banner': [
        {
            'block_type':  'image_baner',
            'image':       'corporate_banner.jpg',
            'title':       'Корпоративним клієнтам',
            'text':        '',
            'button_text': '',
            'button_url':  'https://youtu.be/nsmYbQqZEA8?si=JR7tQiORnHZ1ElvR',
        }
    ],
    'image_footer_banner': [
        {
            'block_type':  'image_baner',
            'image':       'corporate_footer.jpg',
            'title':       'Зв\'язатись з нами',
            'text':        '',
            'button_text': 'Контакти',
            'button_url':  'https://youtu.be/nsmYbQqZEA8?si=JR7tQiORnHZ1ElvR',
        }
    ],
    'content_block': [
        {
            'block_type':  'content_block',
            'image':       'corporate_content.jpg',
            'title':       'Наші переваги',
            'body_text':   '<p>Переваги для корпоративних клієнтів</p>',
            'button_text': '',
            'button_url':  '',
        }
    ],
}

# ── DeliveryPaymentPage ─────────────────────────────────────────────────
DELIVERY_PAGE_IMAGES = {
    'image_top_banner': [
        {
            'block_type':  'image_baner',
            'image':       'delivery_banner.jpg',
            'title':       'Доставка і оплата',
            'text':        '',
            'button_text': '',
            'button_url':  '',
        }
    ],
    'content_block': [
        {
            'block_type':  'content_block',
            'image':       'delivery_content.jpg',
            'title':       'Умови доставки',
            'body_text':   '<p>Опис умов доставки та оплати</p>',
            'button_text': '',
            'button_url':  '',
        }
    ],
}

# ── OrderPlaced ─────────────────────────────────────────────────────────
ORDER_PAGE = {
    'thanks_title': 'Дякуємо за замовлення!',
    'banner_title': 'Ми зв\'яжемось з вами найближчим часом',
}
ORDER_PAGE_IMAGES = {
    'image_banner': [
        {
            'block_type':  'image_baner',
            'image':       'order_banner.jpg',
            'title':       'Дякуємо!',
            'text':        'Ваше замовлення прийнято',
            'button_text': 'На головну',
            'button_url':  'None',
        }
    ],
}

# ── Прості сторінки (без картинок) ─────────────────────────────────────
NEWS_LIST_PAGE = {
    'title_page': '<p>Новини</p>',
    'subtitle':   '<p>Останні події</p>',
}

GALLERY_PAGE = {}  # заповнюється вручну через адмін

USER_AGREEMENT_PAGE = {
    'text': '<p>Текст користувацької угоди</p>',
}