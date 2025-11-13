from django.urls import path

from users.views import admin_login, admin_logout
from adminpanel.views import dashboard, admin_404, orders, customers, products

app_name = 'adminpanel'

urlpatterns = [
    path('login/', admin_login, name='login'),
    path('logout/', admin_logout, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('orders/', orders, name='orders'),
    path('customers/', customers, name='customers'),
    path('products/', products, name='products'),
    path('404/', admin_404, name='admin_404'),
]