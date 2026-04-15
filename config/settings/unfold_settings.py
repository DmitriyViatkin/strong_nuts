from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy

def is_manager(user):
    return user.is_authenticated and (user.groups.filter(name="managers").exists() or user.is_superuser)

def is_inventory_admin(user):
    return user.is_authenticated and (user.groups.filter(name="admins").exists() or user.is_superuser)

UNFOLD = {
    "SITE_TITLE": "Nuts Admin",
    "SITE_HEADER": "Nuts",
    "SITE_SYMBOL": "nutrition",

    "DASHBOARD_CALLBACK": "unfold_admin.views.dashboard_callback",

    "SITE_DROPDOWN": [
        {
            "icon": "open_in_new",
            "title": _("Відкрити сайт"),
            "link": "http://127.0.0.1:8000/",
            "attrs": {"target": "_blank"},
        },
        {
            "icon": "home",
            "title": _("Головна адмінки"),
            "link": reverse_lazy("admin:index"),
        },
    ],

    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": False,

        "navigation": [
            {
                "title": _("Управление"),
                "separator": True,
                "collapsible": True,
                # Доступно только Суперюзеру
                "permission": lambda r: r.user.is_superuser,
                "items": [
                    {
                        "title": _("Сотрудники"),
                        "icon": "people",
                        "link": "/admin/cabinet/user/?is_staff=1",
                    },
                    {
                        "title": _("Пользователи"),
                        "icon": "badge",
                        "link": "/admin/cabinet/user/?is_staff=0",
                    },
                    {
                        "title": _("Группы и права"),
                        "icon": "admin_panel_settings",
                        "link": reverse_lazy("admin:auth_group_changelist"),
                    },
                ],
            },
            {
                "title": _("Заказы"),
                "separator": True,
                "collapsible": True,
                # Видят Менеджеры и Суперюзеры
                "permission": lambda r: is_manager(r.user),
                "items": [
                    {
                        "title": _("Все заказы"),
                        "icon": "shopping_bag",
                        "link": reverse_lazy(
                            "admin:order_management_clientorder_changelist"),
                        "badge": "unfold_admin.views.orders_badge",
                    },
                    {
                        "title": _("Транзакции"),
                        "icon": "payments",
                        "link": reverse_lazy(
                            "admin:order_management_billingoperation_changelist"),
                    },
                ],
            },
            {
                "title": _("Каталог"),
                "separator": True,
                "collapsible": True,
                # Видят   и Суперюзеры
                "permission": lambda r: is_inventory_admin(r.user),
                "items": [
                    {
                        "title": _("Товары"),
                        "icon": "inventory_2",
                        "link": reverse_lazy(
                            "admin:product_management_product_changelist"),
                    },
                ],
            },
            {
                "title": _("Фоновые задачи"),
                "separator": True,
                "collapsible": True,

                "permission": lambda r: r.user.is_superuser,
                "items": [
                    {
                        "title": _("Результаты задач"),
                        "icon": "task",
                        "link": reverse_lazy(
                            "admin:django_celery_results_taskresult_changelist"),
                    },
                    {
                        "title": _("Результаты групп"),
                        "icon": "lan",
                        "link": reverse_lazy(
                            "admin:django_celery_results_groupresult_changelist"),
                    },
                ],
            },
        ],
    },
}