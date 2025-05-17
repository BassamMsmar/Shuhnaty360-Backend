from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import PaymentVoucher
from .serializers import PaymentVoucherSerializer

# Create your views here.

class PaymentVoucherListCreateView(generics.ListCreateAPIView):
    """عرض قائمة السندات وإنشاء سند جديد"""
    queryset = PaymentVoucher.objects.all()
    serializer_class = PaymentVoucherSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """إنشاء سند جديد"""
        serializer.save(creator=self.request.user)

class PaymentVoucherDetailView(generics.RetrieveUpdateDestroyAPIView):
    """عرض وتحديث وحذف سند"""
    queryset = PaymentVoucher.objects.all()
    serializer_class = PaymentVoucherSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        """تحديث سند"""
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        """تنفيذ التحديث"""
        instance = serializer.save()
        # تحديث حالة الشحنة
        instance.update_status(
            user=self.request.user,
            notes="تم تحديث السند"
        )
