from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test

from orders.models import Order
from users.models import User
from shop.models import Product
from django.db.models import Sum


@login_required(login_url='adminpanel:login')
@user_passes_test(lambda user: user.is_staff, login_url='adminpanel:admin_404', redirect_field_name=None)
def dashboard(request):
    total_orders = Order.objects.count()
    total_revenue = Order.objects.aggregate(Sum('total_amount'))['total_amount__sum']
    total_customers = User.objects.filter(is_staff=False).count()
    total_products = Product.objects.count()
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
    context = {
        'orders': orders,
    }
    return render(request, 'adminpanel/orders.html', context)

def customers(request):
    customers = User.objects.filter(is_staff=False)
    context = {
        'customers': customers,
    }
    return render(request, 'adminpanel/customers.html', context)


def products(request):
    products = Product.objects.all()
    context = {
        'products': products,
    }
    return render(request, 'adminpanel/products.html', context)


def admin_404(request):
    return render(request, 'adminpanel/admin_404.html', status=404)