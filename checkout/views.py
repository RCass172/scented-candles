""" Imports """
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .forms import OrderForm


# Create your views here.
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(
            request, 'There is nothing in your shopping cart yet :(')
        return redirect(reverse('products'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51K6iStLwG2wdS70DoqxoWAZafjeCHQSDndIogoyyp3zK06hSYomHiDWMtZv1bRPwQ6oNQza3nq6Co0D5DPmTBIkM00zD6GNLuk',
        'client_secret': 'test client secret',
    }

    return render(request, template, context)
