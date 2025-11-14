from django.db.models import Avg

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from users.forms import UserRegistrationForm
from shop.models import Product
from api.serializers import ProductListSerializer, OrderListSerializer
from orders.models import Order


@api_view(['POST'])
@permission_classes([AllowAny])
def user_registration(request):
    form = UserRegistrationForm(request.data)
    if form.is_valid():
        user = form.save(commit=False)
        user.username = user.email
        user.save()
        return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
    return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def products_list(request):
    products = Product.objects.filter(is_active=True, is_deleted=False).annotate(avg_rating=Avg('ratings__rating'))
    serializer = ProductListSerializer(products, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def orders_list(request):
    print(request.user)
    orders = Order.objects.filter(user=request.user).prefetch_related('order_items', 'order_items__product')
    serializer = OrderListSerializer(orders, many=True, context={'request': request})
    return Response(serializer.data)