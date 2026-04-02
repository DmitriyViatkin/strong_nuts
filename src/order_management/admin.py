from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin, TabularInline
from .models import ClientOrder, OrderItem, BillingOperation



class OrderItemInline(TabularInline):
    model = OrderItem
    extra = 0
    fields = ("product", "count", "price", "display_total")
    readonly_fields = ("display_total",)

    @admin.display(description=_("Разом"))
    def display_total(self, obj):
        return f"{obj.total} грн." if obj.id else "-"



class BillingOperationInline(TabularInline):
    model = BillingOperation
    extra = 0
    fields = ("status", "amount", "date")
    readonly_fields = ("date",)


@admin.register(ClientOrder)
class ClientOrderAdmin(ModelAdmin):
    list_display = ("id", "user", "status", "delivery", "summary_display", "created_at")
    list_filter = ("status", "delivery", "created_at")
    search_fields = ("id", "user__username", "user__email")
    list_editable = ("status",)


    inlines = [OrderItemInline, BillingOperationInline]

    fieldsets = (
        (_("Інформація про замовлення"), {
            "fields": (("user", "status"), ("delivery", "summary"), "comment"),
        }),
    )

    @admin.display(description=_("Сума"))
    def summary_display(self, obj):
        return f"{obj.summary} грн."


@admin.register(OrderItem)
class OrderItemAdmin(ModelAdmin):

    list_display = ("order", "product", "count", "price")
    list_filter = ("order__status",)
    search_fields = ("order__id", "product__name")


@admin.register(BillingOperation)
class BillingOperationAdmin(ModelAdmin):

    list_display = ("id", "order", "user", "status", "amount", "date")
    list_filter = ("status", "date")
    search_fields = ("order__id", "user__username")