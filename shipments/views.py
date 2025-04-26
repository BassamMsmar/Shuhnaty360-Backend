from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.utils import timezone


from .models import Shipment, ShipmentHistory, ShipmentStatus
from .serializers import ShipmentSerializerList, ShipmentSerializerDetail, ShipmentSerializercreate, ShipmentStatusSerializer

# Create your views here.
class ShipmentListCreateView(generics.ListCreateAPIView):
    queryset = Shipment.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['user', 'driver', 'client','client_branch', 'client_invoice_number', 'recipient', 'status']
    search_fields = ['tracking_number']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ShipmentSerializercreate
        return ShipmentSerializerList
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        shipment = serializer.save()
        # نرجع البيانات باستخدام Serializer العرض
        output_serializer = ShipmentSerializerList(shipment, context={'request': request})
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)



class ShipmentDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializerDetail
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        # جلب الشحنة القديمة
        old_instance = self.get_object()
        old_status = old_instance.status
        
        # تنفيذ التحديث
        updated_instance = serializer.save()

        # طباعة حالة الشحنة قبل وبعد التحديث
        print(f"Old Status: {old_status}, New Status: {updated_instance.status}")

        # تحقق إذا كانت الحالة قد تغيرت
        if old_status != updated_instance.status:
            # إنشاء سجل في ShipmentHistory
            ShipmentHistory.objects.create(
                shipment=updated_instance,
                user=self.request.user,
                status=updated_instance.status,
                updated_at=timezone.now(),
                notes=f"تم تغيير الحالة من {old_status} إلى {updated_instance.status}"
            )
            print("تم إنشاء سجل في ShipmentHistory")

        else:
            print("لم تتغير الحالة، لم يتم إنشاء سجل.")


class ShipmentStatus(generics.ListCreateAPIView):
    queryset = ShipmentStatus.objects.all()
    serializer_class = ShipmentStatusSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['name_ar', 'name_en']
    search_fields = ['name_ar', 'name_en']

    def get(self, request, *args, **kwargs):
        shipment_status = self.get_queryset()
        serializer = self.get_serializer(shipment_status, many=True)
        return Response(serializer.data)