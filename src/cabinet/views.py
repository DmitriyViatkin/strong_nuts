from django.shortcuts import render
from django.views.generic import TemplateView

class MyCabinetView(TemplateView):
    template_name = 'cabinet/account.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Мой кабинет'

        return context