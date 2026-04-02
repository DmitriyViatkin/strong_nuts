from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic   import ListView, DetailView, UpdateView
from django.urls import reverse
from .forms import FopUserForm, RegularUserForm
from order_management.models import ClientOrder, BillingOperation, OrderItem
from django.contrib.auth.mixins import LoginRequiredMixin


class MyCabinetView(TemplateView):
    template_name = 'cabinet/account.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Мой кабинет'

        return context



class ListBillingOperations(LoginRequiredMixin, ListView):

    model = BillingOperation
    template_name = 'cabinet/history-trans.html'
    context_object_name = 'billing_operations'

    def get_queryset(self):
        """
        Повертає список транзакцій для поточного користувача.
         Відсортований за датою створення (найновіші перші).
         """
        return (BillingOperation.objects.filter(user=self.request.user)
                .select_related('order').order_by('-id'))

class ListClientOrders(LoginRequiredMixin, ListView):

    model = ClientOrder
    template_name = 'cabinet/history.html'
    context_object_name = 'client_orders'

    def get_queryset(self):
        """
        Повертає список замовлень для поточного користувача.
         Відсортований за датою створення (найновіші перші).
         """
        return (ClientOrder.objects.filter(user=self.request.user)
                .prefetch_related('items__product', 'transactions').order_by('-id'))

class ContactInformation(LoginRequiredMixin, UpdateView):
    template_name = 'cabinet/contact_information.html'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        return self.request.user

    def get_form_class(self):
        if self.request.user.is_fop:
            return FopUserForm
        return RegularUserForm

    def get_success_url(self):
        return reverse('cabinet:contact-information')