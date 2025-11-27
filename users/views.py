import logging

from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth import login, logout, get_user_model
from django.db.models import F, Sum
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.cache import never_cache

from users.forms import UserRegistrationForm, UserLoginForm
from users.models import Cart, CartItem

User = get_user_model()

logger = logging.getLogger('users')


def user_registration(request):
    logger.info(f"Registration page accessed by {request.META.get('REMOTE_ADDR', 'unknown')}")
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            if User.objects.filter(email=form.cleaned_data['email']).exists():
                messages.error(request, 'Email already registered.')
                logger.warning(f"Email already registered: {form.cleaned_data['email']}")
            else:
                user = form.save(commit=False)
                user.username = user.email
                user.save()
                logger.info(f"New user registered: {user.email}")
                login(request, user)
                return redirect('shop:index')
        else:
            logger.warning(f"Registration form validation failed: {form.errors}")
    else:
        form = UserRegistrationForm()
    return render(request, 'users/registration.html', {'form': form})

@never_cache
@user_passes_test(lambda user: not user.is_authenticated, login_url='shop:index', redirect_field_name=None)
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
    return redirect('shop:index')


@login_required(login_url='users:login')
def cart_view(request):
    logger.info(f"Cart viewed by user: {request.user.email}")
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    cart_items = CartItem.objects.filter(cart=cart)
    for cart_item in cart_items:
        if cart_item.product.stock < cart_item.quantity:
            cart_item.quantity = cart_item.product.stock
            cart_item.save()
            logger.warning(f"Stock limit reached: product_id={cart_item.product.id}, stock={cart_item.product.stock}, user={request.user.email}")
            messages.error(request, f'Sorry, only {cart_item.product.stock} {cart_item.product.name}(s) left in stock.')
        if cart_item.quantity <= 0 or not cart_item.product.is_active or cart_item.product.is_deleted:
            cart_item.delete()
            logger.warning(f"Item deleted from cart: product_id={cart_item.product.id}, user={request.user.email}")
            messages.error(request, 'Some items in your cart are no longer available.')
    
    cart_items = CartItem.objects.filter(cart=cart).annotate(subtotal=F('quantity') * F('product__price'))
    total = cart_items.aggregate(total=Sum(F('subtotal')))['total']
    if total is None:
        total = 0
    context = {
        'cart': cart,
        'cart_items': cart_items if cart_items else None,
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


@never_cache
@user_passes_test(lambda user: not user.is_authenticated, login_url='adminpanel:dashboard', redirect_field_name=None)
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
