from django.urls import path

from config.urls import urlpatterns
from .views import page_not_found


urlpatterns = [

    path('404/', Page404View.as_view(), name='404')

]