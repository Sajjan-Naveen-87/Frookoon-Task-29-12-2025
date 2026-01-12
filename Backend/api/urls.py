from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import (
    UserSignupView, 
    ProductListView, 
    OrderCreateView,
    OrderListView,
    OrderDetailView,
    HealthCheckView
)

urlpatterns = [
    # Authentication endpoints
    path('auth/signup/', UserSignupView.as_view(), name='signup'),
    path('auth/token/', obtain_auth_token, name='api_token_auth'),
    
    # Product endpoints
    path('products/', ProductListView.as_view(), name='product-list'),
    
    # Order endpoints
    path('orders/', OrderCreateView.as_view(), name='order-create'),       # POST - Create order
    path('orders/', OrderListView.as_view(), name='order-list'),           # GET - List user orders
    path('orders/<uuid:pk>/', OrderDetailView.as_view(), name='order-detail'),  # GET - Order details
    
    # Health check
    path('health/', HealthCheckView.as_view(), name='health-check'),
]

