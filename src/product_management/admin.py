from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from unfold.admin import TabularInline
from  unfold.admin import ModelAdmin
from .models import Product, Gallery

class GalleryInline(TabularInline):
    model = Product.gallery.through

    extra = 1
    verbose_name = _("Фото в галереї")
    verbose_name_plural = _("Галерея товару")

@admin.register(Gallery)
class GalleryAdmin(ModelAdmin):
    list_display = ("display_image", "image")

    @admin.display(description=_("Предпросмотр изображения"))
    def display_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="100" height="100" />')
        return _("Нет изображения")


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    # 1. Исправлено: добавил is_active и убрал stock
    list_display = ('name', 'price', 'is_active')

    # 2. Исправлено: фильтруем по реальным полям
    list_filter = ('price', 'is_active', 'packaging')

    # 3. Исправлено: поиск по артикулу (проверь, что в модели articul, а не article)
    search_fields = ('name', 'articul')

    # 4. Исправлено: теперь is_active есть в list_display, так что его можно редактировать
    list_editable = ("is_active",)

    fieldsets = (
        (_("Основная информация"), {
            "fields": (("name", "articul"), "summary", "description"),
        }),
        (_("Характеристики"), {
            "fields": (("price", "mass"), ("packaging", "expiration_date"),
                       "composition", "energy_value"),
        }),
        (_("Медиа и статус"), {
            "fields": ("gallery", "is_active"),
        }),
    )


    @admin.display(description=_("Цена"))
    def display_price(self, obj):
        return f"{obj.price} грн."

    @admin.display(description=_("Статус"), boolean=True)
    def stock_status(self, obj):
        return obj.is_active