from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin
from .models import User, Address



@admin.register(Address)
class AddressAdmin(ModelAdmin):
    list_display = ("__str__", "address_type", "city", "company_name")
    list_filter = ("address_type", "country")
    search_fields = ("city", "street", "company_name", "edrpou")


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):


    list_display = ("email", "first_name", "last_name", "phone", "is_fop", "is_staff")
    list_filter = ("is_fop", "is_staff", "is_active")
    search_fields = ("email", "first_name", "last_name", "phone")
    ordering = ("email",)


    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Персональна інформація"),
         {"fields": (("first_name", "last_name"), "phone", "avatar")}),
        (_("Тип клієнта"), {"fields": ("is_fop", "address")}),
        (_("Права доступу"), {
            "fields": ("is_active", "is_staff", "is_superuser", "groups",
                       "user_permissions"),
        }),
        (_("Важливі дати"), {"fields": ("last_login", "date_joined")}),
    )


    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "is_staff", "is_active"),
        }),
    )

    filter_horizontal = ("groups", "user_permissions")