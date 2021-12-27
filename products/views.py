"""imports"""
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower
from django.contrib.auth.decorators import login_required
from .models import Product, Category, Review
from .forms import ProductForm, ReviewForm
from profiles.models import UserProfile


# Create your views here.
def all_products(request):
    """ A view to show all products including in sort and search """

    products = Product.objects.all()
    item = None
    categories = None
    sort = None
    direction = None

    if request.GET:
        if 'q' in request.GET:
            item = request.GET['q']
            if not item:
                messages.error(request, 'Please enter search term')
                return redirect(reverse('products'))

            queries = Q(name__icontains=item) | Q(description__icontains=item)
            products = products.filter(queries)

        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name'

            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_item': item,
        'current_categories': categories,
        'current_sorting': current_sorting,
    }

    return render(request, 'products/products.html', context)


def product_info(request, product_id):
    """ A view to show information of specific product """

    product = get_object_or_404(Product, pk=product_id)

    review_form = ReviewForm()

    context = {
        'product': product,
        'review_form': review_form,
    }

    return render(request, 'products/product_info.html', context)


@login_required
def add_product(request):
    """ Add product to the shop """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, shop owners allowed only.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(
                request, 'Your product has been added successfully')
            return redirect(reverse('product_info', args=[product.id]))
        else:
            messages.error(
                request, 'Sorry, product not added. Please check form is entered correctly.')
    else:
        form = ProductForm()

    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """ Edit a product in shop """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, shop owners allowed only.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(
                request, 'Your product has been added successfully')
            return redirect(reverse('product_info', args=[product.id]))
        else:
            messages.error(
                request, 'Sorry, product not updated. Please check form is entered correctly.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)


@login_required
def del_product(request, product_id):
    """ Delete a product from the store """
    if not request.user.is_superuser:
        messages.error(
            request, 'Sorry, product not deleted. Please check form is entered correctly.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(
        request, 'Your product has been deleted successfully')
    return redirect(reverse('products'))


def add_review(request, product_id):
    """ Add review to product """
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            product = Product.objects.get(pk=product_id)
            profile = UserProfile.objects.get(user=request.user)
            review.product = product
            review.profile = profile
            review.save()
            messages.success(request, 'Your Review Has Been Added')
        else:
            messages.error(
                request, 'Sorry, review not added. Please check form is entered correctly.')
    return redirect(reverse('product_info', args=[product_id]))
