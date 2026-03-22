from wagtail.blocks import StructBlock, CharBlock, ListBlock, URLBlock
from wagtail.images.blocks import  ImageChooserBlock

class MessengerBlock(StructBlock):
    name = CharBlock(lable='Назва')
    link = URLBlock(lable="Посилання")

    class Meta:
        icon = "link"
        label = 'Месенджер'

class NavLinkBlock(StructBlock):
    name = CharBlock(label='Назва')
    link = URLBlock(label='Посилання')

    class Meta:
        icon = 'link'
        label = 'Пункт меню'


class SocialLinkBlock(StructBlock):
    name = CharBlock(label='Назва')
    icon = ImageChooserBlock(label='Іконка')
    URL_link = URLBlock(label='Посилання')

    class Meta:
        icon = 'link'
        label = 'Соцмережа'


class PhoneBlock(StructBlock):
    number_1 = CharBlock(label='Номер 1')
    number_2 = CharBlock(label='Номер 2', required=False)

    class Meta:
        icon = 'mobile-alt'
        label = 'Телефони'


class AddressBlock(StructBlock):
    name = CharBlock(label='Назва')
    address = CharBlock(label='Адреса')
    icon = ImageChooserBlock(label='Іконка', required=False)

    class Meta:
        icon = 'home'
        label = 'Адреса'