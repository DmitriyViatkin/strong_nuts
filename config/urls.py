from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

urlpatterns = [

    path('admin/',      admin.site.urls),
    path('cms/',        include(wagtailadmin_urls)),
    path('documents/',  include(wagtaildocs_urls)),

]

# З мовним префіксом /uk/, /en/, /ru/
urlpatterns += i18n_patterns(
    path('accounts/', include('accounts.urls')),
    path('cabinet/', include('cabinet.urls')),
    path('', include(wagtail_urls)),
)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
handler404 = 'cms_pages.views.page_not_found'