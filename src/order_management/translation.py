from wagtail_modeltranslation.translation import TranslationOptions, register
from .models import ClientOrder, OrderItem, BillingOperation

@register(ClientOrder)
class ClientOrderTranslationOptions(TranslationOptions):
    fields = (
        'recipient_name',
        'phone',
        'email',
        'company',
        'delivery_address',
        'np_city_ref',
        'np_warehouse_ref',
        'np_warehouse_description',
        'tracking_number',
        'comment',
    )

@register(OrderItem)
class OrderItemTranslationOptions(TranslationOptions):
    fields = (
        # Власних текстових полів тут немає,
        # переклад робиться у моделі Product
    )

@register(BillingOperation)
class BillingOperationTranslationOptions(TranslationOptions):
    fields = (
        # Тут також немає текстових полів для перекладу
    )
