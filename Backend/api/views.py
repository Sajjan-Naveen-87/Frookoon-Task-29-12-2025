from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction
from .models import User, Product, Order, OrderItem, Stock, Address
from .serializers import (
    UserSerializer, ProductSerializer, OrderSerializer, 
    OrderListSerializer, OrderCreateSerializer, OrderDetailSerializer,
    StandardErrorSerializer
)
from django.shortcuts import get_object_or_404


class UserSignupView(generics.CreateAPIView):
    """
    POST /api/v1/auth/signup/
    
    Register a new user in the system.
    
    Request Body:
    {
        "username": "john_doe",
        "phone": "+1234567890",
        "password": "securepassword123"
    }
    
    Response (201 Created):
    {
        "id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
        "username": "john_doe",
        "phone": "+1234567890"
    }
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class ProductListView(generics.ListAPIView):
    """
    GET /api/v1/products/
    
    Retrieves a list of all available products with filtering support.
    
    Query Parameters:
    - category: Filter by exact category match
    - search: Search in product name
    
    Response (200 OK):
    {
        "count": 2,
        "results": [...]
    }
    """
    queryset = Product.objects.filter(is_available=True)
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = Product.objects.filter(is_available=True)
        category = self.request.query_params.get('category')
        search = self.request.query_params.get('search')
        if category:
            queryset = queryset.filter(category__iexact=category)
        if search:
            queryset = queryset.filter(name__icontains=search)
        return queryset


class OrderListView(generics.ListAPIView):
    """
    GET /api/v1/orders/
    
    Retrieves a list of orders for the authenticated user.
    
    Query Parameters:
    - status: Filter by order status
    
    Response (200 OK):
    {
        "count": 2,
        "results": [...]
    }
    """
    serializer_class = OrderListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Order.objects.filter(user=user).order_by('-created_at')
        
        # Filter by status if provided
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter.upper())
        
        return queryset


class OrderCreateView(generics.CreateAPIView):
    """
    POST /api/v1/orders/
    
    Creates a new order. Requires authentication.
    
    Request Body:
    {
        "address": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
        "items": [
            {"product_id": "p1a2b3c4-...", "quantity": 2}
        ],
        "delivery_fee": "5.00"
    }
    
    Response (201 Created):
    {
        "id": "o1a2b3c4-...",
        "status": "PENDING",
        "total_amount": "10.98",
        ...
    }
    """
    serializer_class = OrderCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        # Custom validation with structured error response
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            error_details = {}
            if hasattr(serializer, 'errors'):
                error_details = serializer.errors
            
            return Response(
                {
                    "error": "validation_error",
                    "message": "Invalid input data",
                    "details": error_details
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        order = serializer.save()
        
        # Return created order with success message
        response_serializer = OrderDetailSerializer(order)
        return Response(
            {
                **response_serializer.data,
                "message": "Order created successfully"
            },
            status=status.HTTP_201_CREATED
        )


class OrderDetailView(generics.RetrieveAPIView):
    """
    GET /api/v1/orders/{order_id}/
    
    Retrieves detailed information about a specific order.
    
    Response (200 OK):
    {
        "id": "o1a2b3c4-...",
        "items": [...],
        ...
    }
    
    Error Responses:
    - 401 Unauthorized: Authentication required
    - 403 Forbidden: Order belongs to different user
    - 404 Not Found: Order does not exist
    """
    serializer_class = OrderDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except Order.DoesNotExist:
            return Response(
                {
                    "error": "not_found",
                    "message": "Order not found",
                    "details": {
                        "detail": f"Order with id {kwargs.get('pk')} does not exist."
                    }
                },
                status=status.HTTP_404_NOT_FOUND
            )


class HealthCheckView(APIView):
    """
    GET /api/v1/health/
    
    Simple health check endpoint.
    
    Response (200 OK):
    {
        "status": "healthy",
        "message": "API is running"
    }
    """
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        return Response({
            "status": "healthy",
            "message": "API is running"
        })

