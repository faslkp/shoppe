from django.contrib import admin

from orders.models import Order, OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'address', 'status', 'total_amount', 'created_at']
    list_filter = ['status']
    search_fields = ['user__username', 'address__address_line_1', 'address__city', 'address__state', 'address__zip_code', 'address__country']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price', 'created_at']
    list_filter = ['created_at']
    search_fields = ['order__user__username', 'product__name']