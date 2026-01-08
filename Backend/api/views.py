from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction
from .models import User, Product, Order, OrderItem
from .serializers import UserSerializer, ProductSerializer, OrderSerializer

class UserSignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = Product.objects.all()
        category = self.request.query_params.get('category')
        search = self.request.query_params.get('search')
        if category:
            queryset = queryset.filter(category__iexact=category)
        if search:
            queryset = queryset.filter(name__icontains=search)
        return queryset

class OrderCreateView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
