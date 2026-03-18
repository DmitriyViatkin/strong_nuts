from django.db import models
from django.db import models
from src.cabinet.models import User

from django.utils.translation import gettext_lazy as _

PACKAGING_CHOICE = [
    ('jar',    _('Банка')),
    ('vacuum', _('Вакуумна')),
    ('box',    _('Коробка')),
]


class Gallery(models.Model):
    image = models.ImageField(
        upload_to='gallery/',
        verbose_name=_('Зображення')
    )


    class Meta:
        verbose_name = _('Зображення')
        verbose_name_plural = _('Галерея')



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
    energy_value = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_('Енергетична цінність')
    )
    expiration_date = models.DateField(
        blank=True, null=True,
        verbose_name=_('Термін придатності')
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_('Ціна')
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