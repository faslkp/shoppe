from django.http import request
from rest_framework import serializers
from shop.models import Product
from orders.models import Order, OrderItem



class ProductListSerializer(serializers.ModelSerializer):
    avg_rating = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    def get_avg_rating(self, obj):
        return obj.avg_rating or 0

    def get_image(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.image.url) if obj.image else None

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'image', 'stock', 'avg_rating']


class OrderItemListSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    subtotal = serializers.SerializerMethodField()

    def get_product(self, obj):
        return {
            'id': obj.product.id,
            'name': obj.product.name,
            'price': obj.product.price,
            'image': self.context.get('request').build_absolute_uri(obj.product.image.url) if obj.product.image else None
        }

    def get_subtotal(self, obj):
        return obj.quantity * obj.price

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price', 'subtotal']


class OrderListSerializer(serializers.ModelSerializer):
    order_items = OrderItemListSerializer(many=True)
    address = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    
    def get_address(self, obj):
        return {
            'id': obj.address.id,
            'address_line_1': obj.address.address_line_1,
            'address_line_2': obj.address.address_line_2,
            'city': obj.address.city,
            'state': obj.address.state,
            'zip_code': obj.address.zip_code,
        }

    def get_status(self, obj):
        return obj.get_status_display()

    class Meta:
        model = Order
        fields = ['id', 'address', 'status', 'total_amount', 'created_at', 'order_items']


