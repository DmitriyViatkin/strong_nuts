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
    success_url = reverse_lazy('orders:order_success')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cart = Cart.objects.filter(user=self.request.user).first()
        context['cart'] = cart
        context['cart_items'] = cart.items.select_related('product') if cart else []

        return context

    def form_valid(self, form):
        cart = Cart(self.request)

        # Проверка на пустую корзину перед созданием заказа
        if not cart:
            return redirect('cart:cart_detail')

        with transaction.atomic():
            # 1. Сначала сохраняем данные формы, но не в БД
            order = form.save(commit=False)

            # 2. Привязываем пользователя, если он залогинен
            if self.request.user.is_authenticated:
                order.user = self.request.user

            # 3. Устанавливаем итоговую сумму из корзины
            order.summary = cart.get_total_price()
            order.save()

            # 4. Переносим товары из корзины в OrderItem
            order_items = []
            for item in cart:
                order_items.append(
                    OrderItem(
                        order=order,
                        product=item['product'],
                        price=item['price'],
                        count=item['quantity']
                    )
                )

            # Используем bulk_create для экономии SQL-запросов
            OrderItem.objects.bulk_create(order_items)

            # 5. Очищаем корзину после успешного заказа
            cart.clear()

        return super().form_valid(form)

    