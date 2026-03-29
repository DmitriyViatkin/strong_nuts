from django.shortcuts import render

from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta

from order_management.models import ClientOrder, BillingOperation
from product_management.models import Product
from cabinet.models import User


def dashboard_callback(request, context):
    now = timezone.now()
    today = now.date()
    month_start = today.replace(day=1)
    week_ago = today - timedelta(days=7)

    # --- KPI ---
    context["total_orders"] = ClientOrder.objects.count()
    context["new_orders"] = ClientOrder.objects.filter(status="new").count()
    context["orders_today"] = ClientOrder.objects.filter(
        created_at__date=today
    ).count()

    context["total_users"] = User.objects.filter(is_staff=False).count()
    context["new_users_month"] = User.objects.filter(
        date_joined__date__gte=month_start
    ).count()

    context["total_products"] = Product.objects.count()
    context["active_products"] = Product.objects.filter(is_active=True).count()

    context["revenue_month"] = BillingOperation.objects.filter(
        status="paid",
        date__date__gte=month_start
    ).aggregate(total=Sum("amount"))["total"] or 0

    context["revenue_week"] = BillingOperation.objects.filter(
        status="paid",
        date__date__gte=week_ago
    ).aggregate(total=Sum("amount"))["total"] or 0

    # --- Последние 5 заказов ---
    context["recent_orders"] = ClientOrder.objects.select_related(
        "user"
    ).order_by("-created_at")[:5]

    return context
def orders_badge(request):
    count = ClientOrder.objects.filter(status="new").count()
    return str(count) if count else ""