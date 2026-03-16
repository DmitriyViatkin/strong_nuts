import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from django.utils.translation import gettext_lazy as _


BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / 'src'))
load_dotenv(BASE_DIR / '.env')

SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost').split(',')

INSTALLED_APPS = [
    #Unfold
    'unfold',
    'unfold.contrib.filters',
    'unfold.contrib.forms',

    #Wagtails
    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.contrib.settings',
    'wagtail.contrib.simple_translation',
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

    #my app
    'accounts',
    'cabinet',
    'product_management',
    'order_management',
    'cms_pages',
    'wagtail_cms',
    'unfold_admin'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD':os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('POSTGRES_HOST0', 'localhost'),
        'PORT': os.getenv('POSTGRES_PORT','5432')
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'uk'

LANGUAGES = [
    ('uk', _("Українська")),
    ('en',_('English')),
    ('ru',_('Русский'))
]


TIME_ZONE = 'Europe/Kyiv'
USE_I18N = True
USE_L10N = True
USE_TZ = True

WAGTAIL_I18N_ENABLED = True

WAGTAIL_CONTENT_LANGUAGES = [
    ('uk', _('Українська')),
    ('en', _('English')),
    ('ru', _('Русский'))

]

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

WAGTAIL_SITE_NAME = "nuts_cms"
WAGTAILADMIN_BASE_URL = "http://localhost:8000"

UNFOLD = {

    'SITE_TITLE':"Nuts Admin",
    'SITE_HEADER': "Nuts",
    'SITE_SYMBOL': "nutrition",
    "NAVIGATION":[
     {
            "title": "Staff",
            "icon": "badge",
            "items": [
                {"title": "Співробітники", "link": "/admin/auth/user/?is_staff=1"},
                {"title": "Групи і права", "link": "/admin/auth/group/"},
            ],
        },
        {
            "title": "Users",
            "icon": "people",
            "link": "/admin/auth/user/?is_staff=0",
        },
        {
            "title": "Orders",
            "icon": "shopping_bag",
            "link": "/admin/orders/order/",
        },
        {
            "title": "Transactions",
            "icon": "payments",
            "link": "/admin/orders/transaction/",
        },
        {
            "title": "Products",
            "icon": "inventory_2",
            "link": "/admin/catalog/product/",
        },
    ],

}