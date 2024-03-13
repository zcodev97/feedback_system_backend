from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.conf import settings
from .models import (Vendor, Payment, PaymentMethod, PaymentCycle)

from core.serializers import CustomUserSerializer


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'


class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = '__all__'


class PaymentCycleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentCycle
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    payment_cycle = PaymentCycleSerializer()
    payment_method = PaymentMethodSerializer()
    class Meta:
        model = Payment
        fields = '__all__'
