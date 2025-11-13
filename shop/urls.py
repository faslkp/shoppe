from django.urls import path

from shop.views import index, product_list, product_detail, add_to_cart

app_name = 'shop'

urlpatterns = [
    path('', index, name='index'),
    path('products/', product_list, name='product_list'),
    path('products/<int:product_id>/', product_detail, name='product_detail'),
    path('products/<int:product_id>/add-to-cart/', add_to_cart, name='add_to_cart'),
]