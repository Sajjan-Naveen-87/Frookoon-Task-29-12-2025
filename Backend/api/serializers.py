from rest_framework import serializers
from .models import User, Vendor, Product, Stock, Address, DeliveryPartner, Order, OrderItem, Payment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'phone', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['id', 'name', 'city', 'latitude', 'longitude', 'is_active']

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['quantity', 'updated_at']

class ProductSerializer(serializers.ModelSerializer):
    vendor = VendorSerializer(read_only=True)
    stock = StockSerializer(read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'price', 'stock', 'is_available', 'vendor']

class DeliveryPartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryPartner
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price_at_time']


class OrderItemWriteSerializer(serializers.ModelSerializer):
    product_id = serializers.UUIDField()

    class Meta:
        model = OrderItem
        fields = ['product_id', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    vendor = VendorSerializer(read_only=True)
    address = AddressSerializer(read_only=True)
    delivery_partner = DeliveryPartnerSerializer(read_only=True)
    items_write = OrderItemWriteSerializer(many=True, write_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'vendor', 'address', 'delivery_partner', 'status', 'total_amount', 'delivery_fee', 'created_at', 'items', 'items_write']
        read_only_fields = ['status', 'total_amount', 'vendor', 'delivery_partner']

    def create(self, validated_data):
        items_data = validated_data.pop('items_write')
        # Ensure the user provides an address for the order
        if 'address' not in validated_data:
            raise serializers.ValidationError("Address is required for an order.")
        
        user = validated_data.get('user')
        if not user:
            raise serializers.ValidationError("User is required.")
        
        order = Order.objects.create(**validated_data)
        total_amount = 0
        
        for item_data in items_data:
            try:
                product = Product.objects.get(id=item_data['product_id'])
            except Product.DoesNotExist:
                raise serializers.ValidationError(f"Product with id {item_data['product_id']} does not exist.")
            
            # Get stock from Stock model (not product)
            try:
                stock = Stock.objects.get(product=product)
            except Stock.DoesNotExist:
                raise serializers.ValidationError(f"No stock information for {product.name}")
                
            # Check if there is enough stock
            if stock.quantity < item_data['quantity']:
                raise serializers.ValidationError(f"Not enough stock for {product.name}")
            
            price_at_time = product.price
            order_item = OrderItem.objects.create(order=order, product=product, quantity=item_data['quantity'], price_at_time=price_at_time)
            total_amount += float(price_at_time) * item_data['quantity']

            # Decrease stock
            stock.quantity -= item_data['quantity']
            stock.save()

        order.total_amount = total_amount
        order.save()
        return order


class PaymentSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)
    class Meta:
        model = Payment
        fields = ['id', 'order', 'method', 'status', 'transaction_id', 'amount']