# signals.py
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .services.cart_services import merge_carts


@receiver(user_logged_in)
def on_user_login(sender, request, user, **kwargs):
    session_key = request.session.get('cart_session_key')
    if session_key:
        merge_carts(user, session_key)
        del request.session['cart_session_key']