import uuid
from .models import Cart, CartItem


def get_or_create_cart(request):
    """Повертає кошик для авторизованого або анонімного користувача."""
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        return cart

    session_key = request.session.get('cart_session_key')
    if not session_key:
        session_key = str(uuid.uuid4())
        request.session['cart_session_key'] = session_key

    cart, _ = Cart.objects.get_or_create(session_key=session_key)
    return cart


def merge_carts(user, session_key):
    """Викликати після логіну — зливає анонімний кошик з кошиком юзера."""
    try:
        anon_cart = Cart.objects.get(session_key=session_key)
    except Cart.DoesNotExist:
        return

    user_cart, _ = Cart.objects.get_or_create(user=user)

    for item in anon_cart.items.select_related('product'):
        user_item, created = CartItem.objects.get_or_create(
            cart=user_cart,
            product=item.product,
            defaults={'quantity': item.quantity}
        )
        if not created:
            user_item.quantity += item.quantity
            user_item.save()

    anon_cart.delete()


def add_to_cart(cart, product, quantity=1):
    item, created = CartItem.objects.get_or_create(
        cart=cart, product=product,
        defaults={'quantity': quantity}
    )
    if not created:
        item.quantity += quantity
        item.save()
    return item


def remove_from_cart(cart, product_id):
    CartItem.objects.filter(cart=cart, product_id=product_id).delete()


def update_quantity(cart, product_id, quantity):
    if quantity <= 0:
        remove_from_cart(cart, product_id)
        return None
    item = CartItem.objects.get(cart=cart, product_id=product_id)
    item.quantity = quantity
    item.save()
    return item


def clear_cart(cart):
    cart.items.all().delete()