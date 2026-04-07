from django.db import models
from cabinet.models import User
from product_management.models import Product
from django.utils.translation import gettext_lazy as _
from cities_light.models import Country, Region, City


PAYMENT_STATUS = [
    ('paid',            _('Оплачено')),
    ('pending_payment', _('Очікує оплати')),
    ('cancelled',       _('Скасовано')),
]

DELIVERY_STATUS = [
    ('NP',  _('Нова пошта')),

    ('courier', _('Курʼєр')),
    ('pickup', _('Самовивіз')),
]

PAYMENT_METHODS_CHOICES = [
    ('liqpay', _('LiqPay / Приват24')),
    ('cashless', _('Безготівковий розрахунок')),
    ('cod', _('Накладений платіж (при отриманні)')),
]
ORDER_STATUS = [
    ('new',        _('Новий')),
    ('processing', _('В обробці')),
    ('shipped',    _('Відправлено')),
    ('delivered',  _('Доставлено')),
    ('cancelled',  _('Скасовано')),
]

class ClientOrder(models.Model):

    # 🔹 Користувач
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders',
        verbose_name=_('Користувач')
    )

    # 🔹 Статуси
    status = models.CharField(
        max_length=20,
        choices=ORDER_STATUS,
        default='new',
        verbose_name=_('Статус замовлення')
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default='pending_payment',
        verbose_name=_('Статус оплати')
    )

    # 🔹 Доставка
    delivery = models.CharField(
        max_length=20,
        choices=DELIVERY_STATUS,
        default='NP',
        verbose_name=_('Тип доставки')
    )

    # 🔹 Контактні дані (snapshot)
    recipient_name = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Ім'я отримувача")
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name=_('Телефон')
    )

    email = models.EmailField(
        max_length=255,
        blank=True,
        verbose_name=_('Email')
    )

    company = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_('Компанія')
    )

    # 🔹 Локація (cities-light snapshot)
    country = models.ForeignKey(
        Country,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Країна')
    )

    region = models.ForeignKey(
        Region,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Регіон')
    )

    city = models.ForeignKey(
        City,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Місто')
    )

    # 🔹 Детальна адреса (курʼєр)
    delivery_address = models.CharField(
        max_length=500,
        blank=True,
        verbose_name=_('Адреса доставки (вулиця, будинок, квартира)')
    )

    # 🔹 Nova Poshta
    np_city_ref = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_('NP City Ref')
    )

    np_warehouse_ref = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_('NP Відділення Ref')
    )

    np_warehouse_description = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_('NP Відділення')
    )

    tracking_number = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_('ТТН')
    )


    # 🔹 Фінанси
    summary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_('Сума замовлення')
    )

    # 🔹 Додатково
    comment = models.TextField(
        blank=True,
        verbose_name=_('Коментар')
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата створення')
    )


    payment_method = models.CharField(
        max_length=32, choices=PAYMENT_METHODS_CHOICES,
        default='liqpay',
        verbose_name=_('Способ оплати')
    )

    class Meta:
        verbose_name = _('Замовлення')
        verbose_name_plural = _('Замовлення')

    def __str__(self):
        return f'Замовлення #{self.id} ({self.recipient_name})'

    def calculate_summary(self):
        return sum(item.total for item in self.items.all())


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


