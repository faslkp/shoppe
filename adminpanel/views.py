import json

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum, Avg
from django.contrib import messages
from django.http import JsonResponse

from orders.models import Order, OrderStatus
from users.models import User
from shop.models import Product
from shop.forms import ProductForm


@login_required(login_url='adminpanel:login')
@user_passes_test(lambda user: user.is_staff, login_url='adminpanel:admin_404', redirect_field_name=None)
def dashboard(request):
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


def orders(request):
    orders = Order.objects.all()
    order_status_choices = [(status, label) for status, label in OrderStatus.choices]
    context = {
        'orders': orders,
        'order_status_choices': order_status_choices,
    }
    return render(request, 'adminpanel/orders.html', context)


def order_status_change(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        order_id = data.get('order_id')
        status = data.get('status')
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return JsonResponse({'message': 'Order not found'}, status=404)
        order.status = status
        order.save()
        return JsonResponse({'status': order.get_status_display()}, status=200)
    return JsonResponse({'message': 'Invalid request'}, status=400)


def customers(request):
    customers = User.objects.filter(is_staff=False)
    context = {
        'customers': customers,
    }
    return render(request, 'adminpanel/customers.html', context)


def products(request):
    products = Product.objects.filter(is_deleted=False).annotate(avg_rating=Avg('ratings__rating'))
    context = {
        'products': products,
    }
    return render(request, 'adminpanel/products.html', context)


def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product created successfully')
            return redirect('adminpanel:products')
        else:
            messages.error(request, 'Failed to create product')
            return render(request, 'adminpanel/product_create.html', {'form': form})
    
    form = ProductForm()
    return render(request, 'adminpanel/product_create.html', {'form': form})


def product_update(request, product_id):
    try:
        product = Product.objects.get(id=product_id, is_deleted=False)
    except Product.DoesNotExist:
        messages.error(request, 'Product not found')
        return redirect('adminpanel:products')
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully')
            return redirect('adminpanel:products')
        else:
            messages.error(request, 'Failed to update product')
            return render(request, 'adminpanel/product_create.html', {'form': form})
    else:
        form = ProductForm(instance=product)
        return render(request, 'adminpanel/product_create.html', {'form': form})


def product_status_change(request, product_id):
    try:
        product = Product.objects.get(id=product_id, is_deleted=False)
    except Product.DoesNotExist:
        messages.error(request, 'Product not found')
        return redirect('adminpanel:products')
    product.is_active = not product.is_active
    product.save()
    messages.success(request, 'Product status changed successfully')
    return redirect('adminpanel:products')


def product_delete(request, product_id):
    try:
        product = Product.objects.get(id=product_id, is_deleted=False)
    except Product.DoesNotExist:
        messages.error(request, 'Product not found')
        return redirect('adminpanel:products')
    product.is_deleted = True
    product.is_active = False
    product.save()
    messages.success(request, 'Product deleted successfully')
    return redirect('adminpanel:products')

def admin_404(request):
    return render(request, 'adminpanel/admin_404.html', status=404)