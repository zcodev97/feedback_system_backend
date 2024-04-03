from django.db.models import Sum
from django.forms import model_to_dict
from django.utils.dateparse import parse_date
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from .models import (FeedBack)
from .serializers import (FeedBackSerializer, FeedBackCreateSerializer)
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from core.models import User
from django.utils.html import format_html
import datetime
import pandas as pd
import numpy as np
from django.db.models import Q
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class FeedBackAPI(generics.ListCreateAPIView):
    queryset = FeedBack.objects.all()
    serializer_class = FeedBackSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]


class CreateFeedBackAPI(generics.ListCreateAPIView):
    queryset = FeedBack.objects.all()
    serializer_class = FeedBackCreateSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]


class FeedBackReportAPI(generics.ListAPIView):
    serializer_class = FeedBackSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    paginator = PageNumberPagination()
    paginator.page_size = None  # Set page size to None to disable pagination

    def get_queryset(self):
        queryset = FeedBack.objects.all()
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')

        if date_from and date_to:
            try:
                date_from = parse_date(date_from)
                date_to = parse_date(date_to)
                if date_from and date_to:
                    queryset = queryset.filter(
                        created_at__range=[date_from, date_to])

            except (ValueError, TypeError) as e:
                # Handle invalid date format errors gracefully
                return Response({'error': f'Invalid date format: {str(e)}'}, status=400)

        return queryset
