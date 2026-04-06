import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from cabinet.models import User
from product_management.models import Product


class Cart(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='cart',
        verbose_name=_('Користувач')
    )
    session_key = models.CharField(
        max_length=64,
        null=True, blank=True,
        unique=True,
        verbose_name=_('Ключ сесії')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Кошик')
        verbose_name_plural = _('Кошики')

    def __str__(self):
        return f'Кошик {self.user or self.session_key}'

    @property
    def total(self):
        return sum(item.total for item in self.items.select_related('product'))

    @property
    def total_quantity(self):
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name=_('Кошик')
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name=_('Товар')
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name=_('Кількість'))
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Елемент кошика')
        verbose_name_plural = _('Елементи кошика')
        unique_together = ('cart', 'product')

    def __str__(self):
        return f'{self.product} × {self.quantity}'

    @property
    def total(self):
        return self.product.price * self.quantity
