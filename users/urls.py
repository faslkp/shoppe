from django.urls import path

from users.views import user_registration, user_login, user_logout, user_profile, cart_view, remove_from_cart, decrease_cart_quantity, increase_cart_quantity

app_name = 'users'

urlpatterns = [
    path('register/', user_registration, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('profile/', user_profile, name='profile'),
    path('cart/', cart_view, name='cart'),
    path('cart/remove/<int:cart_item_id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/decrease/<int:cart_item_id>/', decrease_cart_quantity, name='decrease_cart_quantity'),
    path('cart/increase/<int:cart_item_id>/', increase_cart_quantity, name='increase_cart_quantity'),
]