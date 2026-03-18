from django.urls import path
from . import views

app_name = 'cabinet'

urlpatterns = [
    path('my_cabinet/', views.MyCabinetView.as_view(), name='my_cabinet'),

]