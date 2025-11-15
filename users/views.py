import logging

from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth import login, logout
from django.db.models import F, Sum
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from users.forms import UserRegistrationForm, UserLoginForm
from users.models import Cart, CartItem

logger = logging.getLogger('users')


def user_registration(request):
    logger.info(f"Registration page accessed by {request.META.get('REMOTE_ADDR', 'unknown')}")
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.email
            user.save()
            logger.info(f"New user registered: {user.email}")
            return redirect('shop:index')
        else:
            logger.warning(f"Registration form validation failed: {form.errors}")
    else:
        form = UserRegistrationForm()
    return render(request, 'users/registration.html', {'form': form})


def user_login(request):
    logger.info(f"Login page accessed by {request.META.get('REMOTE_ADDR', 'unknown')}")
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            logger.info(f"User logged in: {user.email}")
            return redirect('shop:index')
        else:
            logger.warning(f"Login failed for email: {request.POST.get('username', 'unknown')}")
    else:
        form = UserLoginForm(request)
    return render(request, 'users/login.html', {'form': form})


def user_logout(request):
    if request.user.is_authenticated:
        logger.info(f"User logged out: {request.user.email}")
    logout(request)
    return redirect('shop:index')


@login_required(login_url='users:login')
def user_profile(request):
    pass


@login_required(login_url='users:login')
def cart_view(request):
    logger.info(f"Cart viewed by user: {request.user.email}")
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart).annotate(subtotal=F('quantity') * F('product__price'))
    total = cart_items.aggregate(total=Sum(F('subtotal')))['total']
    if total is None:
        total = 0
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'total': total
    }
    return render(request, 'users/cart.html', context)


@login_required(login_url='users:login')
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    logger.info(f"Item removed from cart: product_id={cart_item.product.id}, product_name={cart_item.product.name}, user={request.user.email}")
    cart_item.delete()
    messages.success(request, 'Item removed from cart.')
    return redirect('users:cart')


@login_required(login_url='users:login')
def decrease_cart_quantity(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
        logger.info(f"Cart quantity decreased: product_id={cart_item.product.id}, quantity={cart_item.quantity}, user={request.user.email}")
        messages.success(request, 'Quantity decreased.')
    else:
        logger.warning(f"Attempt to decrease quantity below 1: product_id={cart_item.product.id}, user={request.user.email}")
        messages.error(request, 'Quantity cannot be less than 1.')
    return redirect('users:cart')


@login_required(login_url='users:login')
def increase_cart_quantity(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    if cart_item.quantity + 1 > cart_item.product.stock:
        logger.warning(f"Stock limit reached when increasing quantity: product_id={cart_item.product.id}, requested_quantity={cart_item.quantity + 1}, stock={cart_item.product.stock}, user={request.user.email}")
        messages.error(request, f'Sorry, only {cart_item.product.stock} {cart_item.product.name}(s) left in stock.')
    else:
        cart_item.quantity += 1
        cart_item.save()
        logger.info(f"Cart quantity increased: product_id={cart_item.product.id}, quantity={cart_item.quantity}, user={request.user.email}")
        messages.success(request, 'Quantity increased.')
    return redirect('users:cart')


def admin_login(request):
    logger.info(f"Admin login page accessed by {request.META.get('REMOTE_ADDR', 'unknown')}")
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_staff:
                login(request, user)
                logger.info(f"Admin logged in: {user.email}")
                return redirect('adminpanel:dashboard')
            else:
                logger.warning(f"Unauthorized admin access attempt by: {user.email}")
                messages.error(request, 'You are not authorized to access this page.')
                return redirect('adminpanel:login')
        else:
            logger.warning(f"Admin login failed for email: {request.POST.get('username', 'unknown')}")
    else:
        form = UserLoginForm(request)
    return render(request, 'users/login.html', {'form': form})


def admin_logout(request):
    if request.user.is_authenticated:
        logger.info(f"Admin logged out: {request.user.email}")
    logout(request)
    return redirect('adminpanel:login')
