from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from api.views import user_registration, products_list, orders_list

app_name = 'api'

urlpatterns = [
    path('users/register/', user_registration, name='user_registration'),
    path('users/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('products/', products_list, name='products_list'),
    path('orders/', orders_list, name='orders_list'),
]