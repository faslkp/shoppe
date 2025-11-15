import json
import logging

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum, Avg
from django.contrib import messages
from django.http import JsonResponse

from orders.models import Order, OrderStatus
from users.models import User
from shop.models import Product
from shop.forms import ProductForm

logger = logging.getLogger('adminpanel')


@login_required(login_url='adminpanel:login')
@user_passes_test(lambda user: user.is_staff, login_url='adminpanel:admin_404', redirect_field_name=None)
def dashboard(request):
    logger.info(f"Admin dashboard accessed by: {request.user.email}")
    total_orders = Order.objects.count()
    total_revenue = Order.objects.aggregate(Sum('total_amount'))['total_amount__sum']
    total_customers = User.objects.filter(is_staff=False).count()
    total_products = Product.objects.filter(is_deleted=False).count()
    recent_orders = Order.objects.order_by('-created_at')[:5]
    context = {
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'total_customers': total_customers,
        'total_products': total_products,
        'recent_orders': recent_orders,
    }
    return render(request, 'adminpanel/dashboard.html', context)


@login_required(login_url='adminpanel:login')
@user_passes_test(lambda user: user.is_staff, login_url='adminpanel:admin_404', redirect_field_name=None)
def orders(request):
    orders = Order.objects.all()
    order_status_choices = [(status, label) for status, label in OrderStatus.choices]
    logger.info(f"Admin orders list viewed by: {request.user.email}, count={orders.count()}")
    context = {
        'orders': orders,
        'order_status_choices': order_status_choices,
    }
    return render(request, 'adminpanel/orders.html', context)


@login_required(login_url='adminpanel:login')
@user_passes_test(lambda user: user.is_staff, login_url='adminpanel:admin_404', redirect_field_name=None)
def order_status_change(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        order_id = data.get('order_id')
        status = data.get('status')
        try:
            order = Order.objects.get(id=order_id)
            old_status = order.status
            order.status = status
            order.save()
            logger.info(f"Order status changed: order_id={order_id}, old_status={old_status}, new_status={status}, admin={request.user.email}")
            return JsonResponse({'status': order.get_status_display()}, status=200)
        except Order.DoesNotExist:
            logger.error(f"Order not found for status change: order_id={order_id}, admin={request.user.email}")
            return JsonResponse({'message': 'Order not found'}, status=404)
    logger.warning(f"Invalid request for order status change: admin={request.user.email}")
    return JsonResponse({'message': 'Invalid request'}, status=400)


@login_required(login_url='adminpanel:login')
@user_passes_test(lambda user: user.is_staff, login_url='adminpanel:admin_404', redirect_field_name=None)
def customers(request):
    customers = User.objects.filter(is_staff=False)
    logger.info(f"Admin customers list viewed by: {request.user.email}, count={customers.count()}")
    context = {
        'customers': customers,
    }
    return render(request, 'adminpanel/customers.html', context)


@login_required(login_url='adminpanel:login')
@user_passes_test(lambda user: user.is_staff, login_url='adminpanel:admin_404', redirect_field_name=None)
def products(request):
    products = Product.objects.filter(is_deleted=False).annotate(avg_rating=Avg('ratings__rating'))
    logger.info(f"Admin products list viewed by: {request.user.email}, count={products.count()}")
    context = {
        'products': products,
    }
    return render(request, 'adminpanel/products.html', context)


@login_required(login_url='adminpanel:login')
@user_passes_test(lambda user: user.is_staff, login_url='adminpanel:admin_404', redirect_field_name=None)
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            logger.info(f"Product created: product_id={product.id}, product_name={product.name}, admin={request.user.email}")
            messages.success(request, 'Product created successfully')
            return redirect('adminpanel:products')
        else:
            logger.warning(f"Product creation failed: {form.errors}, admin={request.user.email}")
            messages.error(request, 'Failed to create product')
            return render(request, 'adminpanel/product_create.html', {'form': form})
    
    logger.info(f"Product create page accessed by: {request.user.email}")
    form = ProductForm()
    return render(request, 'adminpanel/product_create.html', {'form': form})


@login_required(login_url='adminpanel:login')
@user_passes_test(lambda user: user.is_staff, login_url='adminpanel:admin_404', redirect_field_name=None)
def product_update(request, product_id):
    try:
        product = Product.objects.get(id=product_id, is_deleted=False)
    except Product.DoesNotExist:
        logger.error(f"Product not found for update: product_id={product_id}, admin={request.user.email}")
        messages.error(request, 'Product not found')
        return redirect('adminpanel:products')
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            logger.info(f"Product updated: product_id={product_id}, product_name={product.name}, admin={request.user.email}")
            messages.success(request, 'Product updated successfully')
            return redirect('adminpanel:products')
        else:
            logger.warning(f"Product update failed: product_id={product_id}, errors={form.errors}, admin={request.user.email}")
            messages.error(request, 'Failed to update product')
            return render(request, 'adminpanel/product_create.html', {'form': form})
    else:
        logger.info(f"Product update page accessed: product_id={product_id}, admin={request.user.email}")
        form = ProductForm(instance=product)
        return render(request, 'adminpanel/product_create.html', {'form': form})


@login_required(login_url='adminpanel:login')
@user_passes_test(lambda user: user.is_staff, login_url='adminpanel:admin_404', redirect_field_name=None)
def product_status_change(request, product_id):
    try:
        product = Product.objects.get(id=product_id, is_deleted=False)
        old_status = product.is_active
        product.is_active = not product.is_active
        product.save()
        logger.info(f"Product status changed: product_id={product_id}, old_status={old_status}, new_status={product.is_active}, admin={request.user.email}")
        messages.success(request, 'Product status changed successfully')
        return redirect('adminpanel:products')
    except Product.DoesNotExist:
        logger.error(f"Product not found for status change: product_id={product_id}, admin={request.user.email}")
        messages.error(request, 'Product not found')
        return redirect('adminpanel:products')


@login_required(login_url='adminpanel:login')
@user_passes_test(lambda user: user.is_staff, login_url='adminpanel:admin_404', redirect_field_name=None)
def product_delete(request, product_id):
    try:
        product = Product.objects.get(id=product_id, is_deleted=False)
        product.is_deleted = True
        product.is_active = False
        product.save()
        logger.info(f"Product deleted: product_id={product_id}, product_name={product.name}, admin={request.user.email}")
        messages.success(request, 'Product deleted successfully')
        return redirect('adminpanel:products')
    except Product.DoesNotExist:
        logger.error(f"Product not found for deletion: product_id={product_id}, admin={request.user.email}")
        messages.error(request, 'Product not found')
        return redirect('adminpanel:products')


def admin_404(request):
    logger.warning(f"Admin 404 page accessed by: {request.user.email if request.user.is_authenticated else 'anonymous'}")
    return render(request, 'adminpanel/admin_404.html', status=404)