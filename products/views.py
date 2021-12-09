from django.shortcuts import render, get_object_or_404
from .models import Product


# Create your views here.
def all_products(request):
    """ A view to show all products including in sort and search """

    products = Product.objects.all()

    context = {
        'products': products,
    }

    return render(request, 'products/products.html', context)


def product_info(request, product_id):
    """ A view to show information of specific product """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_info.html', context)
