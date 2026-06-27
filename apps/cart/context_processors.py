from .cart import Cart


def cart_context(request):
    cart = Cart(request)
    return {
        'cart': cart,
        'cart_total_items': cart.get_total_items(),
        'cart_total_price': cart.get_total_price(),
    }
