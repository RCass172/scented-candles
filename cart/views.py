""" imports """
from django.shortcuts import (
    render, redirect, reverse, HttpResponse)
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from .models import Coupon
from .forms import CouponApplyForm


# Create your views here.
def view_cart(request):
    """ A view to render the shopping cart """
    return render(request, 'cart/cart.html')


def add_to_cart(request, item_id):
    """ A view to add products to cart """
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    cart = request.session.get('cart', {})

    if item_id in list(cart.keys()):
        cart[item_id] += quantity
    else:
        cart[item_id] = quantity

    request.session['cart'] = cart

    return redirect(redirect_url)


def adjust_cart(request, item_id):
    """Adjust the quantity of product to the specified amount"""

    quantity = int(request.POST.get('quantity'))
    cart = request.session.get('cart', {})

    if quantity > 0:
        cart[item_id] = quantity
    else:
        cart.pop(item_id)

    request.session['cart'] = cart
    return redirect(reverse('view_cart'))


def remove_from_cart(request, item_id):
    """Remove item from the shopping cart"""

    try:
        cart = request.session.get('cart', {})

        cart.pop(item_id)

        request.session['cart'] = cart
        return HttpResponse(status=200)

    except Exception as e:
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
