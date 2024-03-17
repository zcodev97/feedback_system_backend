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


class CreatePaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['payment_cycle'] = instance.payment_cycle.title
        representation['payment_method'] = instance.payment_method.title
        return representation

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        payment_cycle_title = data.get('payment_cycle')
        payment_method_title = data.get('payment_method')

        if payment_cycle_title:
            payment_cycle = PaymentCycle.objects.filter(title=payment_cycle_title).first()
            if payment_cycle:
                internal_value['payment_cycle'] = payment_cycle.id
            else:
                raise serializers.ValidationError({'payment_cycle': 'Payment cycle not found.'})

        if payment_method_title:
            payment_method = PaymentMethod.objects.filter(title=payment_method_title).first()
            if payment_method:
                internal_value['payment_method'] = payment_method.id
            else:
                raise serializers.ValidationError({'payment_method': 'Payment method not found.'})

        return internal_value


class PaidOrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaidOrders
        fields = '__all__'
