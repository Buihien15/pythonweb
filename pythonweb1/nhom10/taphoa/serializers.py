from rest_framework import serializers
from .models import Order, OrderItem, ShippingAddress, Payment, Product, Customer

class CheckoutItemSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField()

class ShippingInfoSerializer(serializers.Serializer):
    address = serializers.CharField()

class CheckoutSerializer(serializers.Serializer):
    items = CheckoutItemSerializer(many=True)
    shipping = ShippingInfoSerializer()
    total = serializers.DecimalField(max_digits=10, decimal_places=2)
    payment_method = serializers.CharField()
