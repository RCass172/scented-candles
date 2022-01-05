""" imports """
from decimal import Decimal
from django.shortcuts import get_object_or_404
from products.models import Product
from .models import Coupon


def cart_contents(request):
    """ Allows cart functionality across all apps """

    coupon_id = request.session.get('coupon_id', int())
    cart_products = []
    total = 0
    product_count = 0
    coupon_total = 0
    cart = request.session.get('cart', {})

    # Checks the coupon code against the coupon model
    try:
        code = Coupon.objects.get(id=coupon_id)

    except Coupon.DoesNotExist:
        code = None

    for item_id, quantity in cart.items():

        product = get_object_or_404(Product, pk=item_id)
        total += quantity * product.price

        # Applies the discount when code found
        if code is not None:
            discount = (code.amount/Decimal('100'))*total
            coupon_total = total - discount
        else:
            coupon_total = total

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

    grand_total = delivery + coupon_total

    context = {
        'cart_products': cart_products,
        'total': total,
        'product_count': product_count,
        'code': code,
        'coupon_total': coupon_total,
        'delivery': delivery,
        'grand_total': grand_total,
    }

    return context
