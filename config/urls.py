from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from product_management import urls as product_urls
from cart import urls as cart_urls
from accounts import urls as accounts_urls
from order_management import urls as order_urls



urlpatterns = [

    path('admin/',      admin.site.urls),
    path('cms/',        include(wagtailadmin_urls)),
    path('documents/',  include(wagtaildocs_urls)),
path('i18n/',       include('django.conf.urls.i18n')),

]

# З мовним префіксом /uk/, /en/, /ru/
urlpatterns += i18n_patterns(
    path('accounts/', include('accounts.urls')),
    path('cabinet/', include('cabinet.urls')),
    path('cart/', include((cart_urls, 'cart'))),
    path('products/', include(product_urls)),
    path('orders/', include((order_urls, 'orders'))),
    path('api/', include('cms_pages.urls')),

    path('', include(wagtail_urls)),
prefix_default_language=True,

)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
handler404 = 'cms_pages.views.page_not_found'