import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _



BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(BASE_DIR / 'src'))
load_dotenv(BASE_DIR / '.env')

SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost').split(',')

AUTH_USER_MODEL = 'cabinet.User'
LOGIN_REDIRECT_URL = 'cabinet:my_cabinet'

INSTALLED_APPS = [
    #Unfold
    'unfold',
    'unfold.contrib.filters',
    'unfold.contrib.forms',
    'django_vite',
    'ninja',

    #Wagtails

    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.contrib.settings',
    'wagtail_modeltranslation',
    'wagtail_modeltranslation.makemigrations',
    'wagtail_modeltranslation.migrate',

    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail',
    'modelcluster',
    'taggit',

    #Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'django_celery_results',
'cities_light',

    #my app
    'accounts.apps.AccountsConfig',
    'cabinet',
    'product_management',
    'order_management',
    'cms_pages',
    'wagtail_cms',
    'unfold_admin',

    'cart',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware'
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                #'wagtail.contrib.settings.context_processors.settings_processor',
                'django.template.context_processors.i18n',
                'wagtail.contrib.settings.context_processors.settings',
                'cms_pages.context_processor.cabinet_pages',
                'cms_pages.context_processor.google_maps_api_key',
                'cms_pages.context_processor.translated_urls',

            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


CSRF_TRUSTED_ORIGINS = [
    "https://strong-nuts-nginx.fwwkl2.easypanel.host",
    "https://strong-nuts-web.fwwkl2.easypanel.host",
]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD':os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('POSTGRES_HOST', 'localhost'),
        'PORT': os.getenv('POSTGRES_PORT','5432')
    }
}


GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'uk'

LANGUAGES = [
    ('uk', _('Ukrainian')),
    ('en', _('English')),
    ('ru', _('Russian')),
]

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]


TIME_ZONE = 'Europe/Kyiv'
USE_I18N = True
USE_L10N = True
USE_TZ = True

WAGTAIL_I18N_ENABLED = False



WAGTAIL_CONTENT_LANGUAGES = [
    ('uk', _('Ukrainian')),
    ('en', _('English')),
    ('ru', _('Russian')),
]

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR/'static']

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

WAGTAIL_SITE_NAME = "nuts_cms"
WAGTAILADMIN_BASE_URL = "http://localhost:8000"

CITIES_LIGHT_TRANSLATION_LANGUAGES = ['uk', 'ru', 'en']
CITIES_LIGHT_INCLUDE_COUNTRIES = ['UA']
CITIES_LIGHT_INCLUDE_CITY_TYPES = ['PPL', 'PPLA', 'PPLA2', 'PPLC']



DJANGO_VITE = {
    "default": {
         "dev_mode": True,
        "dev_server_host": "vite",
        "dev_server_port": 5173,
    }
}

from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.templatetags.static import static

UNFOLD = {
    "SITE_TITLE": "Nuts Admin",
    "SITE_HEADER": "Nuts",
    "SITE_SYMBOL": "nutrition",

    "DASHBOARD_CALLBACK": "unfold_admin.views.dashboard_callback",

    "SITE_DROPDOWN": [
        {
            "icon": "open_in_new",
            "title": _("Відкрити сайт"),
            "link": "https://strong-nuts-nginx.fwwkl2.easypanel.host/",
            "attrs": {"target": "_blank"},
        },
        {
            "icon": "home",
            "title": _("Головна адмінки"),
            "link": reverse_lazy("admin:index"),
        },
    ],

    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": False,

        "navigation": [
            {
                "title": _("Управление"),
                "separator": True,
                "collapsible": True,

                "permission": lambda r: r.user.is_superuser,
                "items": [
                    {
                        "title": _("Сотрудники"),
                        "icon": "people",
                        "link": "/admin/cabinet/user/?is_staff=1",
                    },
                    {
                        "title": _("Пользователи"),
                        "icon": "badge",
                        "link": "/admin/cabinet/user/?is_staff=0",
                    },
                    {
                        "title": _("Группы и права"),
                        "icon": "admin_panel_settings",
                        "link": reverse_lazy("admin:auth_group_changelist"),
                    },
                ],
            },
            {
                "title": _("Заказы"),
                "separator": True,
                "collapsible": True,
                # Видят Менеджеры и Суперюзеры
                "permission": lambda r: is_manager(r.user),
                "items": [
                    {
                        "title": _("Все заказы"),
                        "icon": "shopping_bag",
                        "link": reverse_lazy(
                            "admin:order_management_clientorder_changelist"),
                        "badge": "unfold_admin.views.orders_badge",
                    },
                    {
                        "title": _("Транзакции"),
                        "icon": "payments",
                        "link": reverse_lazy(
                            "admin:order_management_billingoperation_changelist"),
                    },
                ],
            },
            {
                "title": _("Каталог"),
                "separator": True,
                "collapsible": True,
                # Видят   и Суперюзеры
                "permission": lambda r: is_inventory_admin(r.user),
                "items": [
                    {
                        "title": _("Товары"),
                        "icon": "inventory_2",
                        "link": reverse_lazy(
                            "admin:product_management_product_changelist"),
                    },
                ],
            },
            {
                "title": _("Фоновые задачи"),
                "separator": True,
                "collapsible": True,

                "permission": lambda r: r.user.is_superuser,
                "items": [
                    {
                        "title": _("Результаты задач"),
                        "icon": "task",
                        "link": reverse_lazy(
                            "admin:django_celery_results_taskresult_changelist"),
                    },
                    {
                        "title": _("Результаты групп"),
                        "icon": "lan",
                        "link": reverse_lazy(
                            "admin:django_celery_results_groupresult_changelist"),
                    },
                ],
            },
        ],
    },
}


def is_manager(user):
    return user.is_authenticated and (
                user.groups.filter(name="managers").exists() or user.is_superuser)


def is_inventory_admin(user):
    return user.is_authenticated and (
                user.groups.filter(name="admins").exists() or user.is_superuser)

# Media
MEDIA_URL="/media/"
MEDIA_ROOT = BASE_DIR / "media"