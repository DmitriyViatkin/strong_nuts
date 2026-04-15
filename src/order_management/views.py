from django.shortcuts import render
from django.views.generic   import ListView, DetailView, CreateView
from .models import ClientOrder, BillingOperation, OrderItem
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.db import transaction
from .forms import OrderCreateForm
from cart.models import Cart
from cms_pages.models import OrderPlaced

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

    def get_success_url(self):
        page = OrderPlaced.objects.live().first()
        if page:
            return page.url
        return reverse_lazy('cabinet:history-orders')

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



class RepeatOrderView(LoginRequiredMixin, View):

    def post(self, request, pk):
        original = get_object_or_404(ClientOrder, pk=pk)

        if original.user != request.user:
            messages.error(request, 'Немає доступу до цього замовлення.')
            return redirect('cabinet:history-orders',  )

        with transaction.atomic():
            new_order = ClientOrder.objects.create(
                user=original.user,
                delivery=original.delivery,
                recipient_name=original.recipient_name,
                phone=original.phone,
                email=original.email,
                company=original.company,
                country=original.country,
                region=original.region,
                city=original.city,
                delivery_address=original.delivery_address,
                np_city_ref=original.np_city_ref,
                np_warehouse_ref=original.np_warehouse_ref,
                np_warehouse_description=original.np_warehouse_description,
                payment_method=original.payment_method,
                comment=original.comment,
                status='new',
                payment_status='pending_payment',
                tracking_number='',
                summary=0,
            )

            OrderItem.objects.bulk_create([
                OrderItem(
                    order=new_order,
                    product=item.product,
                    count=item.count,
                    price=item.price,
                )
                for item in original.items.select_related('product').all()
            ])

            new_order.summary = new_order.calculate_summary()
            new_order.save(update_fields=['summary'])

        messages.success(request, f'Замовлення #{new_order.id} створено на основі #{original.id}.')
        return redirect('cabinet:history-orders',  )