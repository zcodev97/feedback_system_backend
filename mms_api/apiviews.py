from django.db.models import Sum
from django.utils.dateparse import parse_date
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from .models import (Vendor)
from .serializers import (VendorSerializer)
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings

import datetime
import pandas as pd
import pandas_gbq


class ContainerAPI(generics.ListCreateAPIView):
  #   # Execute SQL query and load data into DataFrame
  #   df = pandas_gbq.read_gbq("""
  #   SELECT o.id ,o.totalValue , o.subTotal,o.created_at, v.arName
  # FROM `peak-brook-355811.food_prod_public.orders` o inner  join  `peak-brook-355811.food_prod_public.vendors`  v on
  # o.vendorID = v.id
  #  LIMIT 10
  #   """,
  #                            project_id='peak-brook-355811')
  #   print(df)
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]


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
