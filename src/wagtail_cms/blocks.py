from wagtail.blocks import StructBlock, CharBlock, ListBlock, URLBlock, StructBlockValidationError, RichTextBlock
from wagtail.images.blocks import  ImageChooserBlock
from wagtail import blocks

class MessengerBlock(StructBlock):
    name = CharBlock(label='Назва (viber, telegram, watsap)')
    link = URLBlock(label="Посилання")

    class Meta:
        icon = "link"
        label = 'Месенджер'

class NavLinkBlock(StructBlock):
    name = CharBlock(label='Назва')
    page = blocks.PageChooserBlock(required=False)
    url = URLBlock(label='Посилання')

    def clean(self,value):
        if not value.get('page') and not value.get('url'):
            raise StructBlockValidationError("Вкажіть сторінку або URL")
        return value

    class Meta:
        icon = 'link'
        label = 'Пункт меню'


class SocialLinkBlock(StructBlock):
    name = CharBlock(label='Назва (facebook, instagram, youtube)')
    link = URLBlock(label="Посилання")

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

class VideoBannerBlock(StructBlock):  # 👈 добавили
    image = ImageChooserBlock(label="Фонове зображення")
    video_url = URLBlock(label="Посилання на відео")
    title = CharBlock(max_length=255, label="Заголовок")
    text = RichTextBlock(
        label="Текст",
        features=['bold', 'italic', 'link', 'ul'],
        help_text="Додайте опис для банера")

    class Meta:
        template = "cms_pages/blocks/video_banner_block.html"
        icon = "media"
        label = "Відео банер"

class StatisticItemBlock(StructBlock):
    number = CharBlock(label='Число (например: 240)')
    unit = CharBlock(label='Одиниця (Га, %, шт)', required=False)
    description = CharBlock(label='Опис')
    sub_description = CharBlock(label='Підопис', required=False)

    class Meta:
        icon = 'list-ul'
        label = 'Статистика'