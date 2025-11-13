from django.contrib import admin
from .models import Product, ProductRating


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['name', 'description']
    list_editable = ['price', 'stock']
    list_per_page = 10
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']
    fields = ['name', 'description', 'price', 'image', 'stock', 'created_at', 'updated_at']
    list_display_links = ['name']


@admin.register(ProductRating)
class ProductRatingAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['product__name', 'user__username']
    list_per_page = 10
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']
    fields = ['product', 'user', 'rating', 'review', 'created_at', 'updated_at']
    list_display_links = ['product', 'user']