from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

from shop.models import Product
from users.models import Cart, CartItem

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
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    if product.stock <= 0:
        messages.error(request, 'Sorry, this product is out of stock.')
        return redirect('shop:product_detail', product_id=product_id)
    
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'quantity': 1})
    if not created and cart_item.quantity + 1 >= product.stock:
        messages.error(request, f'Sorry, only {product.stock} {product.name}(s) left in stock.')
        return redirect('shop:product_detail', product_id=product_id)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    messages.success(request, f'{product.name} has been added to your cart.')
    return redirect('shop:product_detail', product_id=product_id)