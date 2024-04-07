from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.conf import settings
from .models import (FeedBack)

from core.serializers import CustomUserSerializer


class FeedBackSerializer(serializers.ModelSerializer):

    class Meta:
        model = FeedBack
        fields = '__all__'


class FeedBackCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedBack
        fields = ['welcome',   'service_level',
                  'price_level',  'food_level', 'clean_level',
                  'client_name', 'notes', 'client_number']
