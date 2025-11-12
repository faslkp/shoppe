from django.urls import path

from users.views import user_registration, user_login, user_logout, user_cart

app_name = 'users'

urlpatterns = [
    path('register/', user_registration, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('cart/', user_cart, name='cart'),
]