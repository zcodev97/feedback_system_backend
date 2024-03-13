from django.db.models import Sum
from django.utils.dateparse import parse_date
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from .models import (Vendor, Payment, PaymentCycle, PaymentMethod)
from .serializers import (VendorSerializer, PaymentSerializer, PaymentCycleSerializer, PaymentMethodSerializer)
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from core.models import User

import datetime
import pandas as pd
import pandas_gbq


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

# class CompaniesListAPI(generics.ListAPIView):
#     queryset = Company.objects.all()
#     serializer_class = CompanySerializer
#     permission_classes = [IsAuthenticated, DjangoModelPermissions]
#
#
# class CompanyCreateAPI(generics.CreateAPIView):
#     queryset = Company.objects.all()
#     serializer_class = CompanyCreateSerializer
#     permission_classes = [IsAuthenticated, DjangoModelPermissions]
#
#
# class DepositAPI(generics.ListCreateAPIView):
#     queryset = Deposit.objects.all()
#     serializer_class = DepositSerializer
#     permission_classes = [IsAuthenticated, DjangoModelPermissions]
#
#
# class DepositCreateAPI(generics.CreateAPIView):
#     queryset = Deposit.objects.all()
#     serializer_class = DepositCreateSerializer
#     permission_classes = [IsAuthenticated, DjangoModelPermissions]
#
#
# class WithdrawAPI(generics.ListCreateAPIView):
#     queryset = Withdraw.objects.all()
#     serializer_class = WithdrawSerializer
#     permission_classes = [IsAuthenticated, DjangoModelPermissions]
#
#
# class WithdrawTypeAPI(generics.ListCreateAPIView):
#     queryset = WithdrawType.objects.all()
#     serializer_class = WithdrawTypeSerializer
#     permission_classes = [IsAuthenticated, DjangoModelPermissions]
#
#
# class CreateWithdrawTypeAPI(generics.CreateAPIView):
#     queryset = WithdrawType.objects.all()
#     serializer_class = WithdrawTypeSerializer
#     permission_classes = [IsAuthenticated, DjangoModelPermissions]
#
#
# class WithdrawCreateAPI(generics.CreateAPIView):
#     queryset = Withdraw.objects.all()
#     serializer_class = WithdrawCreateSerializer
#     permission_classes = [IsAuthenticated, DjangoModelPermissions]
#
#
# class WithdrawsReportAPI(generics.ListCreateAPIView):
#     serializer_class = WithdrawSerializer
#     permission_classes = [IsAuthenticated, DjangoModelPermissions]
#
#     def get_queryset(self):
#         queryset = Withdraw.objects.all()
#         date_from = self.request.query_params.get('date_from')
#         date_to = self.request.query_params.get('date_to')
#         if date_from and date_to:
#             date_from = parse_date(date_from)
#             date_to = parse_date(date_to)
#             if date_from and date_to:
#                 queryset = queryset.filter(
#                     created_at__range=[date_from, date_to])
#
#         return queryset
#
#
# class DepositsReportAPI(generics.ListCreateAPIView):
#     serializer_class = DepositSerializer
#     permission_classes = [IsAuthenticated, DjangoModelPermissions]
#
#     def get_queryset(self):
#         queryset = Deposit.objects.all()
#         date_from = self.request.query_params.get('date_from')
#         date_to = self.request.query_params.get('date_to')
#         if date_from and date_to:
#             date_from = parse_date(date_from)
#             date_to = parse_date(date_to)
#             if date_from and date_to:
#                 queryset = queryset.filter(
#                     created_at__range=[date_from, date_to])
#
#         return queryset
#
#
# class ContainerDepositAPI(generics.ListCreateAPIView):
#     serializer_class = DepositSerializer
#     permission_classes = [IsAuthenticated, DjangoModelPermissions]
#
#     def get_queryset(self):
#         # Assuming you get the container_id from the request's query parameters
#
#         container_id = self.kwargs['pk']
#         if container_id:
#             # If container_id is provided, filter deposits for that specific container
#             queryset = Deposit.objects.filter(container__id=container_id)
#         else:
#             # If no container_id is provided, return all deposits
#             queryset = Deposit.objects.all()
#
#         return queryset
#
#
# class ContainerWithdrawsAPI(generics.ListCreateAPIView):
#     serializer_class = WithdrawSerializer
#     permission_classes = [IsAuthenticated, DjangoModelPermissions]
#
#     def get_queryset(self):
#         # Assuming you get the container_id from the request's query parameters
#         container_id = self.kwargs['pk']
#
#         if container_id:
#             # If container_id is provided, filter deposits for that specific container
#             queryset = Withdraw.objects.filter(container__id=container_id)
#
#         else:
#             # If no container_id is provided, return all deposits
#             queryset = Withdraw.objects.all()
#
#         return queryset
#
#
# class CompanyDepositAPI(generics.ListCreateAPIView):
#     serializer_class = DepositSerializer
#     permission_classes = [IsAuthenticated, DjangoModelPermissions]
#
#     def get_queryset(self):
#         company_name_id = self.kwargs['pk']
#
#         if company_name_id:
#             # If container_id is provided, filter deposits for that specific container
#             queryset = Deposit.objects.filter(company_name_id=company_name_id)
#         else:
#             # If no container_id is provided, return all deposits
#             queryset = Deposit.objects.all()
#         return queryset
#
#
# class CompanyWithdrawsAPI(generics.ListCreateAPIView):
#     serializer_class = WithdrawSerializer
#     permission_classes = [IsAuthenticated, DjangoModelPermissions]
#
#     def get_queryset(self):
#         # Assuming you get the container_id from the request's query parameters
#         company_name_id = self.kwargs['pk']
#
#         if company_name_id:
#             # If container_id is provided, filter deposits for that specific container
#             queryset = Withdraw.objects.filter(company_name_id=company_name_id)
#         else:
#             # If no container_id is provided, return all deposits
#             queryset = Withdraw.objects.all()
#
#         return queryset
#
#
# class CompanySupervisorAPI(generics.ListCreateAPIView):
#     serializer_class = CompanySerializer
#     permission_classes = [IsAuthenticated, DjangoModelPermissions]
#
#     def get_queryset(self):
#         # Assuming you get the container_id from the request's query parameters
#         supervisor = self.kwargs['pk']
#
#         if supervisor:
#             # If container_id is provided, filter deposits for that specific container
#             queryset = Company.objects.filter(supervisor=supervisor)
#         else:
#             # If no container_id is provided, return all deposits
#             queryset = Company.objects.all()
#
#         return queryset
#
#
# class SupervisorWithdrawsAPI(generics.ListCreateAPIView):
#     serializer_class = WithdrawSerializer
#     permission_classes = [IsAuthenticated, DjangoModelPermissions]
#
#     def get_queryset(self):
#         # Assuming you get the container_id from the request's query parameters
#         supervisor_id = self.kwargs['pk']
#
#         if supervisor_id:
#             # If container_id is provided, filter deposits for that specific container
#             queryset = Withdraw.objects.filter(supervisor_id=supervisor_id)
#         else:
#             # If no container_id is provided, return all deposits
#             queryset = Withdraw.objects.all()
#
#         return queryset
#
#
# class SupervisorDepositsAPI(generics.ListCreateAPIView):
#     serializer_class = DepositSerializer
#     permission_classes = [IsAuthenticated, DjangoModelPermissions]
#
#     def get_queryset(self):
#         # Assuming you get the container_id from the request's query parameters
#         supervisor_id = self.kwargs['pk']
#
#         if supervisor_id:
#             # If container_id is provided, filter deposits for that specific container
#             queryset = Deposit.objects.filter(supervisor_id=supervisor_id)
#         else:
#             # If no container_id is provided, return all deposits
#             queryset = Deposit.objects.all()
#
#         return queryset
