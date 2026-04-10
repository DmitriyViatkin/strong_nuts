from django.db import models
from django.db import models
from cabinet.models import User

from django.utils.translation import gettext_lazy as _

PACKAGING_CHOICE = [
    ('jar',    _('Банка')),
    ('vacuum', _('Вакуумна')),
    ('box',    _('Коробка')),
]
FLAVOR_CATEGORIES_CHOICE = [
    ('sweet',   _('Сладкие и десертные')),
    ('savory',  _('Соленые и пикантные')),
    ('spicy',   _('Пряные и необычные')),
]


class Gallery(models.Model):
    image = models.ImageField(
        upload_to='gallery/',
        verbose_name=_('Зображення')
    )
    

    class Meta:
        verbose_name = _('Зображення')
        verbose_name_plural = _('Галерея')

    def __str__(self):
        return f"Image{self.id}"



class Product(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name=_('Назва')
    )
    summary = models.CharField(
        max_length=500,
        blank=True,
        verbose_name=_('Короткий опис')
    )
    description = models.TextField(
        blank=True,
        verbose_name=_('Опис')
    )
    mass = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_('Маса')
    )
    composition = models.CharField(
        max_length=500,
        blank=True,
        verbose_name=_('Склад')
    )
    flavor_categories =   models.CharField(
        max_length=20,
        choices=FLAVOR_CATEGORIES_CHOICE,
        default='sweet',
        verbose_name=_('Смакові Якості')
    )

    energy_value = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_('Енергетична цінність')
    )
    expiration_date = models.DateField(
        blank=True, null=True,
        verbose_name=_('Термін придатності')
    )
    storage_conditions = models.CharField(
        max_length=500,
        blank=True,
        verbose_name=_('Умови зберігання')
    )

    # --- Цены ---
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_('Ціна')
    )
    old_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True, null=True,
        verbose_name=_('Стара ціна')
    )
    is_sale = models.BooleanField(
        default=False,
        verbose_name=_('Акція')
    )

    articul = models.CharField(
        max_length=100,
        unique=True,
        blank=True,
        verbose_name=_('Артикул')
    )
    packaging = models.CharField(
        max_length=20,
        choices=PACKAGING_CHOICE,
        default='jar',
        verbose_name=_('Упаковка')
    )
    gallery = models.ManyToManyField(
        Gallery,
        blank=True,
        verbose_name=_('Галерея')
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Активний')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата створення')
    )

    class Meta:
        verbose_name = _('Товар')
        verbose_name_plural = _('Товари')

    def __str__(self):
        return self.name

    @property
    def discount_percent(self):
        """Считает процент скидки автоматически"""
        if self.is_sale and self.old_price and self.old_price > self.price:
            return int((1 - self.price / self.old_price) * 100)
        return 0