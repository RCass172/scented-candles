from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Product


# Create your views here.
def all_products(request):
    """ A view to show all products including in sort and search """

    products = Product.objects.all()
    item = None

    if request.GET:
        if 'q' in request.GET:
            item = request.GET['q']
            if not item:
                messages.error(request, 'Please enter search term')
                return redirect(reverse('products'))

            queries = Q(name__icontains=item) | Q(description__icontains=item)
            products = products.filter(queries)

    context = {
        'products': products,
        'search_item': item,
    }

    return render(request, 'products/products.html', context)


def product_info(request, product_id):
    """ A view to show information of specific product """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_info.html', context)
