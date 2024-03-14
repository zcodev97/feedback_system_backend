from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.conf import settings
from .models import (Vendor, Payment, PaymentMethod, PaymentCycle, PaidOrders)

from core.serializers import CustomUserSerializer


class VendorCustomSerializer(serializers.ModelSerializer):
    total_to_be_paid = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    orders = serializers.JSONField(read_only=True)

    class Meta:
        model = Vendor
        fields = ['name', 'total_to_be_paid', 'orders']


class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = '__all__'


class PaymentCycleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentCycle
        fields = '__all__'


class VendorSerializer(serializers.ModelSerializer):
    pay_period = PaymentCycleSerializer(read_only=True)  # Assuming this is your payment_cycle serializer
    pay_type = PaymentMethodSerializer(read_only=True)  # Assuming this is your payment_method serializer

    class Meta:
        model = Vendor
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    payment_cycle = PaymentCycleSerializer()
    payment_method = PaymentMethodSerializer()

    class Meta:
        model = Payment
        fields = '__all__'


class PaidOrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaidOrders
        fields = '__all__'
