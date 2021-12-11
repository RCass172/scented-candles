""" imports """


def cart_contents(request):
    """ Allows cart functionality across all apps """

    cart_products = []
    total = 0
    product_count = 0

    delivery = 0

    grand_total = delivery + total

    context = {
        'cart_products': cart_products,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'grand_total': grand_total,
    }

    return context
