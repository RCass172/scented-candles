""" imports """
from django.shortcuts import (
    render, redirect, reverse, get_object_or_404, HttpResponse)
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from products.models import Product
from .models import Coupon
from .forms import CouponApplyForm


# Create your views here.
def view_cart(request):
    """ A view to render the shopping cart """
    return render(request, 'cart/cart.html')


def add_to_cart(request, item_id):
    """ A view to add products to cart """

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    cart = request.session.get('cart', {})

    if item_id in list(cart.keys()):
        cart[item_id] += quantity
        messages.success(
                request, f'Updated {product.name} total is {cart[item_id]}')
    else:
        cart[item_id] = quantity
        messages.success(
            request, f'Successfully added {product.name} to your cart')

    request.session['cart'] = cart

    return redirect(redirect_url)


def adjust_cart(request, item_id):
    """Adjust the quantity of product to the specified amount"""

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    cart = request.session.get('cart', {})

    if quantity > 0:
        cart[item_id] = quantity
        messages.success(
                request, f'Updated {product.name} total is {cart[item_id]}')
    else:
        cart.pop(item_id)
        messages.success(
                request, f'Removed {product.name} from cart')

    request.session['cart'] = cart
    return redirect(reverse('view_cart'))


def remove_from_cart(request, item_id):
    """Remove item from the shopping cart"""

    try:
        product = get_object_or_404(Product, pk=item_id)
        cart = request.session.get('cart', {})

        cart.pop(item_id)
        messages.success(
                request, f'Removed {product.name} from cart')

        request.session['cart'] = cart
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)


@require_http_methods(["GET", "POST"])
def apply_coupon(request):
    coupon_form = CouponApplyForm(request.POST)
    code = request.POST.get('coupon-code')
    try:
        coupon = Coupon.objects.get(code=code, active=True)
        request.session['coupon_id'] = coupon.id
        messages.success(
            request, 'Coupon has been applied')
    except Coupon.DoesNotExist:
        request.session['coupon_id'] = None
        messages.warning(
            request, 'Coupon has not been accepted')
        return redirect('view_cart')
    else:
        return redirect('view_cart')
