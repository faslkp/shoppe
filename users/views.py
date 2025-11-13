from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth import login, logout
from django.db.models import F, Sum
from django.contrib import messages

from users.forms import UserRegistrationForm, UserLoginForm
from users.models import Cart, CartItem

def user_registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.email
            user.save()
            return redirect('shop:index')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/registration.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('shop:index')
    else:
        form = UserLoginForm(request)
    return render(request, 'users/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('shop:index')


def user_profile(request):
    pass


def cart_view(request):
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


def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    cart_item.delete()
    messages.success(request, 'Item removed from cart.')
    return redirect('users:cart')


def decrease_cart_quantity(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
        messages.success(request, 'Quantity decreased.')
    else:
        messages.error(request, 'Quantity cannot be less than 1.')
    return redirect('users:cart')


def increase_cart_quantity(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    if cart_item.quantity + 1 > cart_item.product.stock:
        messages.error(request, f'Sorry, only {cart_item.product.stock} {cart_item.product.name}(s) left in stock.')
    else:
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, 'Quantity increased.')
    return redirect('users:cart')