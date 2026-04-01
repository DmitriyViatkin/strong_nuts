from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic   import ListView, DetailView
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
    template_name = 'billing_operations_list.html'
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
    template_name = 'history.html'
    context_object_name = 'client_orders'

    def get_queryset(self):
        """
        Повертає список замовлень для поточного користувача.
         Відсортований за датою створення (найновіші перші).
         """
        return (ClientOrder.objects.filter(user=self.request.user)
                .prefetch_related('items__product', 'transaction').order_by('-id'))