from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, render
from product_management.models import Product
from .services.cart_services import get_or_create_cart, add_to_cart, remove_from_cart, update_quantity, clear_cart
import json


def cart_detail(request):
    cart = get_or_create_cart(request)
    items = cart.items.select_related('product').all()
    data = {
        'total': str(cart.total),
        'total_quantity': cart.total_quantity,
        'items': [
            {
                'product_id': i.product_id,
                'name': i.product.name,
                'price': str(i.product.price),
                'quantity': i.quantity,
                'total': str(i.total),
            }
            for i in items
        ],
    }
    return JsonResponse(data)


@require_POST
def cart_add(request):
    body = json.loads(request.body)
    product = get_object_or_404(Product, pk=body['product_id'], is_active=True)
    quantity = int(body.get('quantity', 1))
    cart = get_or_create_cart(request)
    item = add_to_cart(cart, product, quantity)
    return JsonResponse({'quantity': item.quantity, 'total': str(cart.total)})


@require_POST
def cart_update(request):
    body = json.loads(request.body)
    cart = get_or_create_cart(request)
    update_quantity(cart, body['product_id'], int(body['quantity']))
    return JsonResponse({'total': str(cart.total), 'total_quantity': cart.total_quantity})


@require_POST
def cart_remove(request):
    body = json.loads(request.body)
    cart = get_or_create_cart(request)
    remove_from_cart(cart, body['product_id'])
    return JsonResponse({'total': str(cart.total), 'total_quantity': cart.total_quantity})


@require_POST
def cart_clear(request):
    cart = get_or_create_cart(request)
    clear_cart(cart)
    return JsonResponse({'status': 'ok'})



def cart_page(request):
    cart = get_or_create_cart(request)
    items = cart.items.select_related('product').all()
    return render(request, 'cart/cart.html', {
        'cart_items': items,
        'cart_total': cart.total,
    })
