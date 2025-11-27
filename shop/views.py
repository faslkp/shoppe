import logging

from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Avg
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.db.models.functions import Random

from shop.models import Product
from users.models import Cart, CartItem
from shop.models import ProductRating

logger = logging.getLogger('shop')

def index(request):
    logger.info(f"Index page accessed by {request.META.get('REMOTE_ADDR', 'unknown')}")
    new_arrivals = Product.objects.filter(is_active=True, is_deleted=False).order_by('-created_at')[:5]
    trending_items = Product.objects.filter(is_active=True, is_deleted=False).annotate(avg_rating=Avg('ratings__rating')).order_by('-avg_rating')[:5]
    special_for_you = Product.objects.filter(is_active=True, is_deleted=False).order_by(Random())[:5]
    context = {
        'new_arrivals': new_arrivals,
        'trending_items': trending_items,
        'special_for_you': special_for_you
    }
    return render(request, 'shop/index.html', context)


def product_list(request):
    products = Product.objects.filter(is_active=True, is_deleted=False)

    q = request.GET.get('q')
    if q:
        products = products.filter(name__icontains=q)
        logger.info(f"Product search performed: query='{q}'")
    
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    min_rating = request.GET.get('min_rating')
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    if min_rating:
        products = products.filter(ratings__rating__gte=min_rating)

    logger.info(f"Product list viewed: count={products.count()}, filters={{'min_price': {min_price}, 'max_price': {max_price}, 'min_rating': {min_rating}}}")
    context = {
        'products': products
    }
    return render(request, 'shop/product_list.html', context)


def product_detail(request, product_id):
    try:
        product = Product.objects.get(id=product_id, is_active=True, is_deleted=False)
        logger.info(f"Product detail viewed: product_id={product_id}, product_name={product.name}")
    except Product.DoesNotExist:
        logger.error(f"Product not found: product_id={product_id}")
        messages.error(request, 'Product not found')
        return redirect('shop:product_list')
    avg_rating = product.ratings.aggregate(Avg('rating'))['rating__avg'] or 0
    count_rating = product.ratings.count() or 0
    context = {
        'product': product,
        'avg_rating': avg_rating,
        'count_rating': count_rating
    }
    return render(request, 'shop/product_detail.html', context)


@login_required(login_url='users:login')
def add_to_cart(request, product_id):
    try:
        product = Product.objects.get(id=product_id, is_active=True, is_deleted=False)
    except Product.DoesNotExist:
        logger.error(f"Product not found when adding to cart: product_id={product_id}, user={request.user.email}")
        messages.error(request, 'Product not found')
        return redirect('shop:product_list')
    cart, created = Cart.objects.get_or_create(user=request.user)

    if product.stock <= 0:
        logger.warning(f"Out of stock attempt: product_id={product_id}, product_name={product.name}, user={request.user.email}")
        messages.error(request, 'Sorry, this product is out of stock.')
        return redirect('shop:product_detail', product_id=product_id)
    
    with transaction.atomic():
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'quantity': 1})
        if not created and cart_item.quantity + 1 >= product.stock:
            logger.warning(f"Stock limit reached: product_id={product_id}, stock={product.stock}, user={request.user.email}")
            messages.error(request, f'Sorry, only {product.stock} {product.name}(s) left in stock.')
            return redirect('shop:product_detail', product_id=product_id)
        if not created:
            cart_item.quantity += 1
        cart_item.save()
        logger.info(f"Product added to cart: product_id={product_id}, product_name={product.name}, quantity={cart_item.quantity}, user={request.user.email}")
        messages.success(request, f'{product.name} has been added to your cart.')
        return redirect('shop:product_detail', product_id=product_id)


@login_required(login_url='users:login')
def rate_product(request, product_id):
    try:
        product = Product.objects.get(id=product_id, is_active=True, is_deleted=False)
    except Product.DoesNotExist:
        logger.error(f"Product not found when rating: product_id={product_id}, user={request.user.email}")
        messages.error(request, 'Product not found')
        return redirect('shop:product_list')
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        rating = request.POST.get('rating')
        ProductRating.objects.update_or_create(
                product=product, 
                user=request.user, 
                defaults={'rating': rating}
            )
        logger.info(f"Product rated: product_id={product_id}, rating={rating}, user={request.user.email}")
        messages.success(request, 'Rating added successfully.')
        return redirect('orders:order_detail', order_id=order_id)
    return redirect('shop:product_detail', product_id=product_id)