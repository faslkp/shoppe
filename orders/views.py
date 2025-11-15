import logging

from django.shortcuts import render
from users.models import Address
from users.models import CartItem
from django.db.models import Sum, F, Subquery, OuterRef
from django.contrib import messages
from django.shortcuts import redirect
from django.db import transaction
from django.contrib.auth.decorators import login_required

from orders.models import Order, OrderItem
from shop.models import ProductRating

logger = logging.getLogger('orders')


@login_required(login_url='users:login')
def checkout_view(request):
    logger.info(f"Checkout page accessed by user: {request.user.email}")
    cart_items = CartItem.objects.filter(cart__user=request.user).annotate(subtotal=F('quantity') * F('product__price'))
    total = cart_items.aggregate(total=Sum(F('subtotal')))['total']

    if request.method == 'POST':
        with transaction.atomic():
            address_id = request.POST.get('selected_address')
            address = None
            if address_id and address_id != 'new':
                try:
                    address = Address.objects.get(id=address_id)
                    logger.info(f"Existing address selected: address_id={address_id}, user={request.user.email}")
                except Address.DoesNotExist:
                    logger.error(f"Invalid address selected: address_id={address_id}, user={request.user.email}")
                    messages.error(request, 'Invalid address selected.')
                    return redirect('orders:checkout')

            if address_id == 'new':
                address = Address.objects.create(
                    user=request.user,
                    address_line_1=request.POST.get('address_line_1'),
                    address_line_2=request.POST.get('address_line_2'),
                    city=request.POST.get('city'),
                    state=request.POST.get('state'),
                    zip_code=request.POST.get('zip_code'),
                    country=request.POST.get('country')
                )
                logger.info(f"New address created: address_id={address.id}, user={request.user.email}")
            
            if request.POST.get('save_address'):
                Address.objects.filter(user=request.user).update(is_default=False)
                address.is_default = True
                address.save()
                logger.info(f"Address set as default: address_id={address.id}, user={request.user.email}")
            
            order = Order.objects.create(user=request.user, address=address, total_amount=total)
            logger.info(f"Order created: order_id={order.id}, total_amount={total}, user={request.user.email}")

            for cart_item in cart_items:
                try:
                    if cart_item.product.stock < cart_item.quantity:
                        cart_item.quantity = cart_item.product.stock
                        cart_item.save()
                        raise Exception(f'Sorry, only {cart_item.product.stock} {cart_item.product.name}(s) left in stock.')
                    
                    OrderItem.objects.create(order=order, product=cart_item.product, quantity=cart_item.quantity, price=cart_item.product.price)

                    cart_item.product.stock -= cart_item.quantity
                    cart_item.product.save()
                    
                    logger.info(f"Order item created: order_id={order.id}, product_id={cart_item.product.id}, quantity={cart_item.quantity}, user={request.user.email}")
                    cart_item.delete()
                except Exception as e:
                    logger.error(f"Error placing order: order_id={order.id}, error={str(e)}, user={request.user.email}")
                    messages.error(request, f'Error placing order: {e}')
                    return redirect('users:cart')
            
            logger.info(f"Order placed successfully: order_id={order.id}, user={request.user.email}")
            messages.success(request, 'Order placed successfully.')
            return redirect('orders:order_detail', order_id=order.id)
    
    addresses = Address.objects.filter(user=request.user)
    context = {
        'addresses': addresses,
        'cart_items': cart_items,
        'total': total
    }
    return render(request, 'orders/checkout.html', context)


@login_required(login_url='users:login')
def orders_view(request):
    orders = Order.objects.filter(user=request.user).select_related('address').prefetch_related(
        'orderitem_set', 'orderitem_set__product').order_by('-created_at')
    logger.info(f"Orders list viewed: user={request.user.email}, count={orders.count()}")
    context = {
        'orders': orders
    }
    return render(request, 'orders/orders.html', context)


@login_required(login_url='users:login')
def order_detail_view(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
        logger.info(f"Order detail viewed: order_id={order_id}, user={request.user.email}")
    except Order.DoesNotExist:
        logger.error(f"Order not found: order_id={order_id}, user={request.user.email}")
        messages.error(request, 'Order not found')
        return redirect('orders:orders')
    user_rating_subquery = Subquery(
        ProductRating.objects.filter(
            product=OuterRef('product'),
            user=request.user
        ).values('rating')[:1]
    )
    order_items = OrderItem.objects.filter(order=order).prefetch_related(
        'product', 'product__ratings').order_by('product__name').annotate(
                subtotal=F('quantity') * F('product__price'),
                user_rating=user_rating_subquery
            )
    context = {
        'order': order,
        'order_items': order_items
    }
    return render(request, 'orders/order_detail.html', context)