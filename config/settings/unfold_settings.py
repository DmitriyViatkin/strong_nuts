from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy



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
                "title": _("Management"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Користувачі"),
                        "icon": "people",
                        "link": "/admin/cabinet/user/?is_staff=1",
                    },
                    {
                        "title": _("Співробітники"),
                        "icon": "badge",
                         "link": "/admin/cabinet/user/?is_staff=0",
                    },
                    {
                        "title": _("Групи і права"),
                        "icon": "admin_panel_settings",
                        "link": reverse_lazy("admin:auth_group_changelist"),
                    },
                ],
            },
            {
                "title": _("Orders"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Замовлення"),
                        "icon": "shopping_bag",
                        "link": reverse_lazy(
                            "admin:order_management_clientorder_changelist"),
                        "badge": "unfold_admin.views.orders_badge",
                    },
                    {
                        "title": _("Транзакції"),
                        "icon": "payments",
                        "link":
                            reverse_lazy(
                                "admin:order_management_billingoperation_changelist"),
                    },
                ],
            },
            {
                "title": _("Catalog"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Товари"),
                        "icon": "inventory_2",
                        "link": reverse_lazy(
                            "admin:product_management_product_changelist"),
                    },
                ],
            },
            {
                "title": _("Celery Tasks"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Task results"),
                        "icon": "task",
                        "link": reverse_lazy(
                            "admin:django_celery_results_taskresult_changelist"
                        ),
                    },
                    {
                        "title": _("Group results"),
                        "icon": "lan",
                        "link": reverse_lazy(
                            "admin:django_celery_results_groupresult_changelist"
                        ),
                    },
                ],
            },
        ],
    },
}