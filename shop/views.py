from django.shortcuts import render
from django.shortcuts import get_object_or_404

from shop.models import Product

def index(request):
    return render(request, 'shop/index.html')


def product_list(request):
    products = Product.objects.all()

    q = request.GET.get('q')
    if q:
        products = products.filter(name__icontains=q)
    
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    min_rating = request.GET.get('min_rating')
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    if min_rating:
        products = products.filter(ratings__rating__gte=min_rating)

    context = {
        'products': products
    }
    return render(request, 'shop/product_list.html', context)


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    context = {
        'product': product
    }
    return render(request, 'shop/product_detail.html', context)


def add_to_cart(request, product_id):
    pass