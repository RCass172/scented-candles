"""Imports"""
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from checkout.models import Order
from .models import UserProfile
from .forms import ProfileForm


# Create your views here.
@login_required
def profile(request):
    """ Display user profile"""
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(
                request, 'Your profile has been updated successfully')
        else:
            messages.error(
                request, 'Sorry, your profile was not updated. '
                         'Please check form is entered correctly.')
    else:
        form = ProfileForm(instance=profile)
    orders = profile.orders.all()
    template = 'profiles/profile.html'
    context = {
        'orders': orders,
        'form': form,
    }

    return render(request, template, context)


def order_history(request, order_number):
    """ Display user order history"""
    order = get_object_or_404(Order, order_number=order_number)

    messages.info(request, (
        f'Your confirmation for previous order number {order_number}. '
        'A confirmation email was sent on the order date.'
    ))

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }

    return render(request, template, context)
