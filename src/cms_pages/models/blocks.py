from wagtail.blocks import (
    StructBlock, CharBlock, RichTextBlock,
    ListBlock, URLBlock, StreamBlock
)
from wagtail.images.blocks import ImageChooserBlock

class ContentBlock(StructBlock):
    """Текстовый блок с изображением — поле content"""
    image = ImageChooserBlock(label='Изображение', required=False)
    title = CharBlock(max_length=255, label='Заголовок')
    body_text = RichTextBlock(label='Текст')
    button_text = CharBlock(max_length=100, required=False, label='Текст кнопки')
    button_url = URLBlock(required=False, label='URL кнопки')
    class Meta:
        icon = 'doc-full'
        label = 'Контент блок'


class BanerBlock(StructBlock):
    """Баннер с изображением — поле image_baner"""
    image = ImageChooserBlock(label='Изображение баннера', required=False)
    title = CharBlock(max_length=255, label='Заголовок')
    text = CharBlock(max_length=500, required=False, label='Текст')
    button_text = CharBlock(max_length=100, required=False, label='Текст кнопки')
    button_url = URLBlock(required=False, label='URL кнопки')

    class Meta:
        icon = 'image'
        label = 'Баннер с изображением'


class NewsBlock(StructBlock):
    """Блок новости — поле news (StreamField[NewsBlock])"""
    image = ImageChooserBlock(label='Изображение', required=False)
    title = CharBlock(max_length=255, label='Заголовок новости')
    date = CharBlock(max_length=50, label='Дата', required=False)
    body = RichTextBlock(label='Текст новости')
    url = URLBlock(required=False, label='Ссылка')

    class Meta:
        icon = 'date'
        label = 'Новость'