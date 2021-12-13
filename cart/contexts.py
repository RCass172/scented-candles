""" imports """
from django.shortcuts import get_object_or_404
from products.models import Product


def cart_contents(request):
    """ Allows cart functionality across all apps """

    cart_products = []
    total = 0
    product_count = 0
    cart = request.session.get('cart', {})

    for item_id, quantity in cart.items():

        product = get_object_or_404(Product, pk=item_id)
        total += quantity * product.price
        product_count += quantity
        cart_products.append({
            'item_id': item_id,
            'quantity': quantity,
            'product': product
        })

    if product_count > 0:
        delivery = 5
    else:
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
