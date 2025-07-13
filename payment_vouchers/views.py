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
from .serializers import PaymentVoucherCreateSerializer, PaymentVoucherListSerializer, PaymentVoucherDetailSerializer, PaymentVoucherOptionsSerializer, PaymentVoucherUpdateSerializer
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
        'approval_status': ['exact'], # if the voucher is approved
        'reviewed_by': ['exact'], # user (the is staff) who approved the voucher
        'receiver_name': ['exact'], # driver name default
        'tracking_number': ['exact'],
        'issuing_branch': ['exact'],
        'client_invoice_number': ['exact'],
        'created_at': ['gte', 'lte'],
    }
    search_fields = ['id', 'tracking_number', 'created_by__username', 'shipment_id']

    def get_queryset(self):
        if self.request.user.is_superuser or   self.request.user.is_staff:
            context = PaymentVoucher.objects.all().order_by('-id')
        else:
            context = PaymentVoucher.objects.filter(created_by=self.request.user).order_by('-id')
        return context

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
    queryset = PaymentVoucher.objects.select_related(
        "shipment",
        "shipment__status",
        "client",
        "client_branch",
        "driver",
        "recipient",
        "origin_city",
        "destination_city",
        "created_by",
        "reviewed_by",
        "issuing_branch"
    )
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


class PaymentVoucherUpdateView(generics.UpdateAPIView):
    """تحديث سند الصرف مع تعديل الحقول المالية والإدارية"""
    queryset = PaymentVoucher.objects.all()
    serializer_class = PaymentVoucherUpdateSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def patch(self, request, *args, **kwargs):
        """تحديث حالة السند وتعديل الحقول المرتبطة"""
        instance = self.get_object()
        new_status = request.data.get('approval_status')

        if new_status not in ['approved', 'rejected', 'pending']:
            return Response({
                'status': 'error',
                'message': 'الحالة المرسلة غير صحيحة. يجب أن تكون: approved أو rejected أو pending.'
            }, status=status.HTTP_400_BAD_REQUEST)

        # تحقق من سبب الرفض إذا كانت الحالة مرفوضة
        if new_status == 'rejected':
            rejection_reason = request.data.get('rejection_reason')

            if not rejection_reason:
                return Response({
                    'status': 'error',
                    'message': 'يرجى كتابة سبب الرفض.'
                }, status=status.HTTP_400_BAD_REQUEST)
            instance.rejection_reason = rejection_reason

        else:
            instance.rejection_reason = None

        instance.approval_status = new_status
        instance.reviewed_by = request.user

        # مرّر بقية الحقول القابلة للتعديل عبر السيريالايزر
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            'status': 'success',
            'message': 'تم تحديث السند بنجاح.',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

        # سجل تاريخ التغيير
        # from .models import PaymentVoucherHistory
        # PaymentVoucherHistory.objects.create(
        #     payment_voucher=instance,
        #     old_status=old_status,
        #     new_status=new_status,
        #     action=new_status,
        #     user=request.user,
        #     notes=instance.rejection_reason if new_status == 'rejected' else ''
        # )

        # return Response({
        #     'status': 'success',
        #     'message': f'تم تحديث حالة السند إلى "{new_status}".',
        #     'data': serializer.data
        # })


 
class PaymentVoucherOptionsView(generics.ListAPIView):
    """عرض قائمة الخيارات لإنشاء سند جديد"""
    queryset = PaymentVoucher.objects.all().order_by('id')
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


   