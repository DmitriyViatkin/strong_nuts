from django.db import models
from cabinet.models import User
from product_management.models import Product
from django.utils.translation import gettext_lazy as _

PAYMENT_STATUS = [
    ('paid',            _('Оплачено')),
    ('pending_payment', _('Очікує оплати')),
    ('cancelled',       _('Скасовано')),
]

DELIVERY_STATUS = [
    ('NP',  _('Нова Пошта')),
    ('UaP', _('Укрпошта')),
    ('MP',  _('Meest Post')),
]

ORDER_STATUS = [
    ('new',        _('Новий')),
    ('processing', _('В обробці')),
    ('shipped',    _('Відправлено')),
    ('delivered',  _('Доставлено')),
    ('cancelled',  _('Скасовано')),
]

class ClientOrder(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='orders',
        verbose_name=_('Користувач')
    )
    status = models.CharField(
        max_length=20,
        choices=ORDER_STATUS,
        default='new',
        verbose_name=_('Статус замовлення')
    )
    delivery = models.CharField(
        max_length=20,
        choices=DELIVERY_STATUS,
        default='NP',
        verbose_name=_('Доставка')
    )
    summary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_('Сума')
    )
    comment = models.TextField(
        blank=True,
        verbose_name=_('Коментар')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата замовлення')
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default='pending_payment',
        verbose_name=_('Статус оплати')
    )
    delivery_address = models.CharField(
        max_length=500, blank=  True, verbose_name= _('Адреса доставки')
    )
    phone = models.CharField(
        max_length=20, blank=True, verbose_name=_('Телефон для доставки')
    )
    recipient_name = models.CharField( max_length= 255, blank=True,
                                       verbose_name=_('Ім\'я отримувача') )

    tracking_number = models.CharField(
        max_length=100, blank=True, verbose_name=_('Номер ТТН)')
         )
    np_city_ref  = models.CharField( max_length=100, blank=True,
                                     verbose_name=_('NP City Ref') )

    np_warehouse_ref = models.CharField( max_length=100, blank=True,
                                        verbose_name=_('NP відділення Ref') )

    np_warehouse_description = models.CharField( max_length=255, blank=True,
                                                verbose_name=_('NP відділення') )
    class Meta:
        verbose_name = _('Замовлення')
        verbose_name_plural = _('Замовлення')

    def __str__(self):
        return f'Замовлення #{self.id} — {self.user}'


class OrderItem(models.Model):
    order = models.ForeignKey(
        ClientOrder,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name=_('Замовлення')
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('Товар')
    )
    count = models.IntegerField(
        default=1,
        verbose_name=_('Кількість')
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_('Ціна на момент замовлення')
    )

    class Meta:
        verbose_name = _('Позиція замовлення')
        verbose_name_plural = _('Позиції замовлення')

    def __str__(self):
        return f'{self.product} x {self.count}'

    @property
    def total(self):
        return self.price * self.count


class BillingOperation(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='transactions',
        verbose_name=_('Користувач')
    )
    order = models.ForeignKey(
        ClientOrder,
        on_delete=models.SET_NULL,
        null=True,
        related_name='transactions',
        verbose_name=_('Замовлення')
    )
    status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default='pending_payment',
        verbose_name=_('Статус оплати')
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_('Сума')
    )
    date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата транзакції')
    )

    class Meta:
        verbose_name = _('Транзакція')
        verbose_name_plural = _('Транзакції')

    def __str__(self):
        return f'#{self.id} — {self.amount} грн — {self.status}'
