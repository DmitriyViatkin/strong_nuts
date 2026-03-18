

from django.contrib.auth.models import AbstractUser, BaseUserManager

from django.db import models
from django.utils.translation import gettext_lazy as _
from cities_light.models import Country, Region, City

class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email обов\'язковий')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, password, **extra_fields)

class Address(models.Model):

    TYPE_PHYSICAL = 'physical'
    TYPE_LEGAL = 'legal'

    ADDRESS_TYPE_CHOICES = [
        (TYPE_PHYSICAL, _('Фізична особа')),
        (TYPE_LEGAL, _('Юридична особа')),
    ]

    # Тип адреси
    address_type = models.CharField(
        max_length=10,
        choices=ADDRESS_TYPE_CHOICES,
        default=TYPE_PHYSICAL,
        verbose_name=_('Тип адреси')
    )

    # Локація через cities-light
    country = models.ForeignKey(
        Country,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name=_('Країна')
    )
    region = models.ForeignKey(
        Region,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name=_('Область')
    )
    city = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_('Місто')
    )

    # Деталі адреси
    street = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_('Вулиця')
    )
    house = models.CharField(
        max_length=20,
        blank=True,
        verbose_name=_('Будинок')
    )
    apartment = models.CharField(
        max_length=20,
        blank=True,
        verbose_name=_('Квартира')
    )
    zip_code = models.CharField(
        max_length=10,
        blank=True,
        verbose_name=_('Поштовий індекс')
    )

    # Для юридичної особи
    company_name = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_('Назва компанії')
    )
    edrpou = models.CharField(
        max_length=10,
        blank=True,
        verbose_name=_('ЄДРПОУ')
    )
    pdv = models.CharField(
        max_length=20,
        blank=True,
        verbose_name=_('ПДВ')
    )

    class Meta:
        verbose_name = _('Адреса')
        verbose_name_plural = _('Адреси')

    def __str__(self):
        parts = filter(None, [
            str(self.country) if self.country else None,
            str(self.region) if self.region else None,
            str(self.city) if self.city else None,
            self.street,
            self.house,
        ])
        return ', '.join(parts)

class User(AbstractUser):

    username = None

    email = models.EmailField(

        unique=True,
        verbose_name= _('Email')
    )
    avatar = models.ImageField(
        upload_to='users/images/',
        blank=True, null=True,
        verbose_name=_('Аватар'),

    )
    phone = models.CharField(
        max_length=13,
        blank=True,
        verbose_name=_('Телефон')
    )
    is_fop = models.BooleanField(
        default=False,
        verbose_name=_('ФОП / Юридична особа')
    )
    address = models.ForeignKey(
        Address,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='users',
        verbose_name=_('Адреса')
    )
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('Користувач')
        verbose_name_plural = _('Користувачі')

    def __str__(self):
        return self.email

    def get_full_name(self):
        if self.is_fop and self.address and self.address.company_name:
            return self.address.company_name
        return f'{self.first_name} {self.last_name}'.strip() or self.email

    @property
    def is_legal(self):
        return self.is_fop