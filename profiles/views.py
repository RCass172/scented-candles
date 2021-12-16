from django.shortcuts import render, get_object_or_404
from .models import UserProfile
from .forms import ProfileForm
from django.contrib import messages


# Create your views here.
def profile(request):
    """ Display user profile"""
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully')

    form = ProfileForm(instance=profile)
    orders = profile.orders.all()
    template = 'profiles/profile.html'
    context = {
        'orders': orders,
        'form': form,
    }

    return render(request, template, context)
