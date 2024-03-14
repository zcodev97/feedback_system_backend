from django.db.models import Sum
from django.forms import model_to_dict
from django.utils.dateparse import parse_date
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from .models import (Vendor, Payment, PaymentCycle, PaymentMethod, PaidOrders)
from .serializers import (VendorSerializer, PaymentSerializer, PaymentCycleSerializer,
                          PaidOrdersSerializer,
                          PaymentMethodSerializer)
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from core.models import User
from django.utils.html import format_html
import datetime
import pandas as pd
import pandas_gbq
import numpy as np


class PaymentMethodAPI(generics.ListCreateAPIView):
    queryset = PaymentMethod.objects.all()
    serializer_class = PaymentMethodSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]


class PaymentCycleAPI(generics.ListCreateAPIView):
    queryset = PaymentCycle.objects.all()
    serializer_class = PaymentCycleSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]


class VendorAPI(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]


class PaymentAPI(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]


class UploadVendorsAsExcel(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

    def create(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        if not file:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            df = pd.read_excel(file)
            for index, row in df.iterrows():

                account_manager = row['account_manager']
                pay_type = row['pay_type']
                pay_period = row['pay_period']

                #               get account manager id
                account_manager_id = User.objects.get(username=account_manager).id
                pay_type_id = PaymentMethod.objects.get(title=pay_type).id
                pay_period_id = PaymentCycle.objects.get(title=pay_period).id

                if Vendor.objects.filter(vendor_id=row['vendor_id']).exists():
                    continue

                vendors = Vendor.objects.create(
                    vendor_id=row['vendor_id'],
                    name=row['name'],
                    account_manager_id=account_manager_id,
                    pay_period_id=pay_period_id,
                    pay_type_id=pay_type_id,
                    number=row['number'],
                    fully_refunded=False,
                    penalized=False,
                    owner_name=row['owner_name'],
                    owner_phone=row['owner_phone'],
                    created_by=request.user,
                )
                vendors.save()

            return Response({'message': 'File Uploaded Successfully'})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VendorPaymentsSummaryAPI(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

    def list(self, request, *args, **kwargs):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        query = f"""
           SELECT * FROM `peak-brook-355811.food_prod_public.vendor_payment` 
           WHERE order_date BETWEEN '{start_date}' AND '{end_date}'
           LIMIT 1000
        """
        df = pandas_gbq.read_gbq(query, project_id='peak-brook-355811')

        # Replace NaN (null in DataFrame) with None for JSON serialization
        # df = df.where(pd.notnull(df), None)

        # Replace NaN (null in DataFrame) with None for direct JSON serialization
        df = df.replace({np.nan: None})

        # Convert the DataFrame to a list of dicts, which is JSON serializable
        data = df.to_dict(orient='records')

        # Group and sum the `to_be_paid` column by vendor
        grouped_sum = df.groupby('vendor', as_index=False)['to_be_paid'].sum()

        # Fetch additional vendor details from the Django model
        vendors = Vendor.objects.prefetch_related('pay_period', 'pay_type').in_bulk(field_name='id')
        vendor_details = {
            vendor.name: {
                'number': vendor.number,
                'penalized': vendor.penalized,
                'fully_refunded': vendor.fully_refunded,
                'pay_period': PaymentCycleSerializer(vendor.pay_period).data.get('title', ''),
                'pay_type': PaymentMethodSerializer(vendor.pay_type).data.get('title', ''),
            } for vendor in vendors.values()
        }

        # Prepare the final results, adding start_date and end_date for each vendor
        final_results = []
        for item in grouped_sum.itertuples(index=False):
            vendor_info = vendor_details.get(item.vendor, {})
            # Update each item with additional vendor details and include start_date and end_date
            result_item = {
                **item._asdict(),
                **vendor_info,
                'start_date': start_date,
                'end_date': end_date,
            }
            final_results.append(result_item)

        return Response([final_results,data])