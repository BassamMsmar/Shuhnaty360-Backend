from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from .models import PaymentVoucher
from .serializers import PaymentVoucherCreateSerializer, PaymentVoucherListSerializer, PaymentVoucherDetailSerializer, PaymentVoucherOptionsSerializer
from shipments.models import Shipment


# Create your views here.

class PaymentVoucherListView(generics.ListAPIView):
    """عرض قائمة السندات وإنشاء سند جديد"""
    queryset = PaymentVoucher.objects.all().order_by('-id')
    serializer_class = PaymentVoucherListSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = {
        'id': ['exact'],
        'shipment': ['exact'],
        'created_by': ['exact'],  # user who created the voucher
        'is_approved': ['exact'], # if the voucher is approved
        'approved_by': ['exact'], # user (the is staff) who approved the voucher
        'receiver_name': ['exact'], # driver name default
        'tracking_number': ['exact'],
        'issuing_branch': ['exact'],
        'created_at': ['gte', 'lte'],
    }
    search_fields = ['id', 'tracking_number', 'created_by__username', 'shipment']

    def perform_create(self, serializer):
        """إنشاء سند جديد"""
        serializer.save(created_by=self.request.user)

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return Response({
            'status': 'success',
            'message': 'Successfully retrieved payment vouchers list',
            'data': response.data
        })



class PaymentVoucherCreateView(generics.CreateAPIView):
    """إنشاء سند جديد"""
    queryset = PaymentVoucher.objects.all()
    serializer_class = PaymentVoucherCreateSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return Response({
            'status': 'success',
            'message': 'Payment voucher created successfully',
            'data': response.data
        })

class PaymentVoucherDetailView(generics.RetrieveAPIView):
    """عرض وحذف سند"""
    queryset = PaymentVoucher.objects.all()
    serializer_class = PaymentVoucherDetailSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]



    def get(self, request, *args, **kwargs):
        """عرض سند"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'status': 'success',
            'message': 'Payment voucher retrieved successfully',
            'data': serializer.data
        })

 
class PaymentVoucherOptionsView(generics.ListAPIView):
    """عرض قائمة الخيارات لإنشاء سند جديد"""
    queryset = PaymentVoucher.objects.all()
    serializer_class = PaymentVoucherOptionsSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]


    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return Response({
            'status': 'success',
            'message': 'Successfully retrieved payment vouchers options',
            'data': response.data
        })

   