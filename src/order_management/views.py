from django.shortcuts import render
from django.views.generic   import ListView, DetailView
from .models import ClientOrder, BillingOperation, OrderItem
from django.contrib.auth.mixins import LoginRequiredMixin


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