from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import PaymentVoucher
from .serializers import PaymentVoucherSerializer

# Create your views here.

class PaymentVoucherListCreateView(generics.ListCreateAPIView):
    """عرض قائمة السندات وإنشاء سند جديد"""
    queryset = PaymentVoucher.objects.all()
    serializer_class = PaymentVoucherSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def perform_create(self, serializer):
        """إنشاء سند جديد"""
        serializer.save(creator=self.request.user)

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return Response({
            'status': 'success',
            'message': 'Successfully retrieved payment vouchers list',
            'data': response.data
        })

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return Response({
            'status': 'success',
            'message': 'Payment voucher created successfully',
            'data': response.data
        })

class PaymentVoucherDetailView(generics.RetrieveUpdateDestroyAPIView):
    """عرض وتحديث وحذف سند"""
    queryset = PaymentVoucher.objects.all()
    serializer_class = PaymentVoucherSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def update(self, request, *args, **kwargs):
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

    def perform_update(self, serializer):
        """تنفيذ التحديث"""
        instance = serializer.save()
        # تحديث حالة الشحنة
        instance.update_status(
            user=self.request.user,
            notes="تم تحديث السند"
        )
