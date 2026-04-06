from django.apps import AppConfig


class CartConfig(AppConfig):
    name = 'cart'

    def redy(self):

        import cart.signals