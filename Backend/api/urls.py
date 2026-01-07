from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import UserSignupView, ProductListView, OrderCreateView

urlpatterns = [
    path('auth/signup/', UserSignupView.as_view(), name='signup'),
    path('auth/token/', obtain_auth_token, name='api_token_auth'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('orders/', OrderCreateView.as_view(), name='order-create'),
]
