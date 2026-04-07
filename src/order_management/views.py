from django.shortcuts import render
from django.views.generic   import ListView, DetailView, CreateView
from .models import ClientOrder, BillingOperation, OrderItem
from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.db import transaction
from .models import ClientOrder, OrderItem
from .forms import OrderCreateForm
from cart.models import Cart

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




class OrderCreateView(CreateView):
    model = ClientOrder
    form_class = OrderCreateForm
    template_name = 'checkout_fiz.html'
    success_url = reverse_lazy('cabinet:history-orders')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cart = Cart.objects.filter(user=self.request.user).first()
        context['cart'] = cart
        context['cart_items'] = cart.items.select_related('product') if cart else []

        return context

    def form_valid(self, form):
        # Отримуємо кошик з БД, а не створюємо об'єкт як обгортку
        cart = Cart.objects.filter(
            user=self.request.user).first() if self.request.user.is_authenticated else None

        if not cart or cart.items.count() == 0:
            return redirect('cart:cart')

        with transaction.atomic():
            order = form.save(commit=False)

            if self.request.user.is_authenticated:
                order.user = self.request.user

            # cart.total — це @property з вашої моделі Cart
            order.summary = cart.total
            order.save()

            order_items = []
            for item in cart.items.select_related('product'):
                order_items.append(
                    OrderItem(
                        order=order,
                        product=item.product,
                        price=item.product.price,
                        count=item.quantity,
                    )
                )

            OrderItem.objects.bulk_create(order_items)

            # Видаляємо всі позиції кошика
            cart.items.all().delete()

        return super().form_valid(form)

class OrderDetailView(DetailView):
    model = ClientOrder
    template_name = 'order.html'
    context_object_name = 'order'

    def get_queryset(self):
        """
        Ограничиваем доступ к заказу только его владельцу.
        """
        return (ClientOrder.objects.filter(user=self.request.user).
                prefetch_related('items__product'))