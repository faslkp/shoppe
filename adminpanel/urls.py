from django.urls import path

from users.views import admin_login, admin_logout
from adminpanel.views import dashboard, admin_404, orders, customers, products, product_create, product_update, product_delete, product_status_change, order_status_change

app_name = 'adminpanel'

urlpatterns = [
    path('login/', admin_login, name='login'),
    path('logout/', admin_logout, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('orders/', orders, name='orders'),
    path('orders/status_change/', order_status_change, name='order_status_change'),
    path('customers/', customers, name='customers'),
    path('products/', products, name='products'),
    path('products/create/', product_create, name='product_create'),
    path('products/update/<int:product_id>/', product_update, name='product_update'),
    path('products/delete/<int:product_id>/', product_delete, name='product_delete'),
    path('products/status_change/<int:product_id>/', product_status_change, name='product_status_change'),
    path('404/', admin_404, name='admin_404'),
]