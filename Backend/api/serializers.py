from rest_framework import serializers
from .models import User, Vendor, Product, Stock, Address, DeliveryPartner, Order, OrderItem, Payment


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model.
    Handles user creation with password hashing.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'phone', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class AddressSerializer(serializers.ModelSerializer):
    """
    Serializer for Address model.
    """
    class Meta:
        model = Address
        fields = ['id', 'user', 'latitude', 'longitude', 'address_line', 'city', 'pincode', 'is_default']
        read_only_fields = ['id', 'user']


class VendorSerializer(serializers.ModelSerializer):
    """
    Serializer for Vendor model (read-only).
    """
    class Meta:
        model = Vendor
        fields = ['id', 'name', 'city', 'latitude', 'longitude', 'is_active']


class StockSerializer(serializers.ModelSerializer):
    """
    Serializer for Stock model (read-only).
    """
    class Meta:
        model = Stock
        fields = ['quantity', 'updated_at']


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for Product model (read-only).
    Includes nested vendor and stock information.
    """
    vendor = VendorSerializer(read_only=True)
    stock = StockSerializer(read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'price', 'stock', 'is_available', 'vendor']


class DeliveryPartnerSerializer(serializers.ModelSerializer):
    """
    Serializer for DeliveryPartner model (read-only).
    """
    class Meta:
        model = DeliveryPartner
        fields = ['id', 'name', 'phone', 'is_active']


class OrderItemSerializer(serializers.ModelSerializer):
    """
    Serializer for OrderItem model (read-only).
    Includes nested product information.
    """
    product = ProductSerializer(read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price_at_time']


class OrderItemWriteSerializer(serializers.ModelSerializer):
    """
    Serializer for creating OrderItem (write-only).
    Validates product existence and stock availability.
    """
    product_id = serializers.UUIDField()
    
    class Meta:
        model = OrderItem
        fields = ['product_id', 'quantity']
    
    def validate_quantity(self, value):
        """Validate that quantity is at least 1."""
        if value < 1:
            raise serializers.ValidationError("Quantity must be at least 1.")
        return value
    
    def validate(self, attrs):
        """Validate product exists and has sufficient stock."""
        product_id = attrs.get('product_id')
        quantity = attrs.get('quantity')
        
        # Check if product exists
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise serializers.ValidationError({
                'product_id': f"Product with id {product_id} does not exist."
            })
        
        # Check if product is available
        if not product.is_available:
            raise serializers.ValidationError({
                'product_id': f"Product '{product.name}' is not available."
            })
        
        # Check stock
        try:
            stock = Stock.objects.get(product=product)
        except Stock.DoesNotExist:
            raise serializers.ValidationError({
                'product_id': f"No stock information for product '{product.name}'."
            })
        
        if stock.quantity < quantity:
            raise serializers.ValidationError({
                'product_id': f"Not enough stock for '{product.name}'. Requested: {quantity}, Available: {stock.quantity}"
            })
        
        attrs['product'] = product
        return attrs


class OrderCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating an Order.
    Handles validation of items, address, and stock availability.
    """
    items = OrderItemWriteSerializer(many=True, write_only=True)
    delivery_fee = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0)
    
    class Meta:
        model = Order
        fields = ['address', 'items', 'delivery_fee']
    
    def validate_items(self, value):
        """Validate that at least one item is provided."""
        if not value or len(value) == 0:
            raise serializers.ValidationError("Order must contain at least one item.")
        return value
    
    def validate_address(self, value):
        """Validate that address exists and belongs to the user."""
        user = self.context['request'].user
        
        if not Address.objects.filter(id=value, user=user).exists():
            raise serializers.ValidationError(
                "Address not found or does not belong to user."
            )
        return value
    
    def create(self, validated_data):
        """Create order with atomic transaction for stock management."""
        items_data = validated_data.pop('items')
        user = self.context['request'].user
        address = validated_data.get('address')
        
        # Use atomic transaction
        from django.db import transaction
        with transaction.atomic():
            # Create the order
            order = Order.objects.create(
                user=user,
                address=address,
                status='PENDING',
                total_amount=0,
                **validated_data
            )
            
            total_amount = 0
            order_items = []
            
            for item_data in items_data:
                product = item_data['product']
                quantity = item_data['quantity']
                price_at_time = product.price
                
                # Create order item
                order_item = OrderItem.objects.create(
                    order=order,
                    product=product,
                    price_at_time=price_at_time,
                    quantity=quantity
                )
                order_items.append(order_item)
                
                total_amount += float(price_at_time) * quantity
                
                # Decrease stock
                stock = Stock.objects.select_for_update().get(product=product)
                stock.quantity -= quantity
                stock.save()
            
            # Update order total
            order.total_amount = total_amount
            order.save()
            
            # Store items for response serialization
            order._order_items = order_items
        
        return order


class OrderListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing orders (minimal information).
    """
    items_count = serializers.SerializerMethodField()
    vendor_name = serializers.CharField(source='vendor.name', read_only=True, default=None)
    
    class Meta:
        model = Order
        fields = [
            'id', 'user', 'vendor', 'vendor_name', 'address', 
            'status', 'total_amount', 'delivery_fee', 
            'created_at', 'items_count'
        ]
        read_only_fields = fields
    
    def get_items_count(self, obj):
        """Get the number of items in the order."""
        return obj.items.count()


class OrderDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for order details (full information).
    Includes nested items, vendor, address, and delivery partner.
    """
    items = OrderItemSerializer(many=True, read_only=True)
    vendor = VendorSerializer(read_only=True)
    address = AddressSerializer(read_only=True)
    delivery_partner = DeliveryPartnerSerializer(read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'user', 'vendor', 'address', 'delivery_partner',
            'status', 'total_amount', 'delivery_fee', 
            'created_at', 'items'
        ]
        read_only_fields = fields


class PaymentSerializer(serializers.ModelSerializer):
    """
    Serializer for Payment model.
    """
    order = OrderSerializer(read_only=True)
    
    class Meta:
        model = Payment
        fields = ['id', 'order', 'method', 'status', 'transaction_id', 'amount']

