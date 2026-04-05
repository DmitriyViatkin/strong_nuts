from django.urls import path
from .views import page_not_found, regions_api

from config.urls import urlpatterns
from .views import page_not_found


urlpatterns = [

    path('404/', page_not_found, name='404'),
    path('regions/', regions_api, name='regions_api'),

]