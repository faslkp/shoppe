from django.urls import path

from orders.views import checkout_view, order_detail_view, orders_view

app_name = 'orders'

urlpatterns = [
    path('checkout/', checkout_view, name='checkout'),
    path('orders/', orders_view, name='orders'),
    path('order/<int:order_id>/', order_detail_view, name='order_detail'),
]
