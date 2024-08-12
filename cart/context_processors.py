from cart.models import Cart


def nb_items(request):

    sub = 0
    user=request.user
    if 'admin' is request.path:
        return {}
    else:
        try:
            cart=user.cart
            for order in cart.orders.all():
                sub+=order.quantity
        except:
            pass

    return dict(sub=sub)

