from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import PaymentVoucher
from .serializers import PaymentVoucherCreateSerializer, PaymentVoucherUpdateSerializer, PaymentVoucherListSerializer, PaymentVoucherDetailSerializer, PaymentVoucherOptionsSerializer

# Create your views here.

class PaymentVoucherListView(generics.ListAPIView):
    """عرض قائمة السندات وإنشاء سند جديد"""
    queryset = PaymentVoucher.objects.all().order_by('-id')
    serializer_class = PaymentVoucherListSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

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

class PaymentVoucherDetailView(generics.RetrieveDestroyAPIView):
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

    def delete(self, request, *args, **kwargs):
        """حذف سند"""
        instance = self.get_object()
        instance.delete()
        return Response({
            'status': 'success',
            'message': 'Payment voucher deleted successfully'
        })


 
class PaymentVoucherUpdateView(generics.UpdateAPIView):
    """تحديث سند"""
    queryset = PaymentVoucher.objects.all()
    serializer_class = PaymentVoucherUpdateSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def put(self, request, *args, **kwargs):
        """تحديث سند"""
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            'status': 'success',
            'message': 'Payment voucher updated successfully',
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
