from django.contrib import admin

from users.models import User, Address, Cart, CartItem

admin.site.register(User)
admin.site.register(Address)
admin.site.register(Cart)
admin.site.register(CartItem)
