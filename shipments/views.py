from typing import override
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.utils import timezone


from .models import Shipment, ShipmentHistory, ShipmentStatus
from .serializers import ShipmentSerializerList, ShipmentSerializerDetail, ShipmentSerializerCreate, ShipmentStatusSerializer, ShipmentSerializerUpdate, ShipmentUpdateStatusSerializer, ShipmentOptionSerializer, ShipmentStatusOptionSerializer, ClientInvoiceNumberOptionSerializer

# Create your views here.

# فصلنا العرض عن الاضافة لان الاضافة يوجد حقول للكتابة فقط
class ShipmentListView(generics.ListAPIView): 
    queryset = Shipment.objects.all().order_by('-id')
    serializer_class = ShipmentSerializerList
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = {
        'user': ['exact'],
        'driver': ['exact'],
        'client': ['exact'],
        'client_branch': ['exact'],
        'recipient': ['exact'],
        'status': ['exact'],
        'origin_city': ['exact'],
        'destination_city': ['exact'],
        'loading_date': ['gte', 'lte'], 
    }
    search_fields = ['tracking_number', 'client_invoice_number', 'id']

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return Shipment.objects.all().order_by('-id')
        else:
            return Shipment.objects.filter(user=self.request.user).order_by('-id')


    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response({
            'status': 'success',
            'message': 'Shipment list retrieved successfully',
            'data': response.data
        })

class ShipmentCreateView(generics.CreateAPIView):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializerCreate
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def create(self, request, *args, **kwargs):
        # استخراج اسم المستخدم
        user_name = request.user.get_full_name() if request.user else "مستخدم غير معروف"
        
        print(request.data)

        # 1. التحقق من البيانات
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 2. إنشاء الشحنة وربطها بالمستخدم
        shipment = serializer.save(user=request.user)

        # 3. إنشاء سجل في تاريخ الشحنة
        ShipmentHistory.objects.create(
            shipment=shipment,
            user=request.user,
            old_status=None,
            new_status=shipment.status,
            action='POST',
            notes=f"قام {user_name} بإنشاء الشحنة بالحالة '{shipment.status}' تلقائيًا",
            updated_at=timezone.now()
        )

        # 4. تحضير الإخراج النهائي
        output_serializer = ShipmentSerializerList(shipment, context={'request': request})
        return Response({
            'status': 'success',
            'message': 'Shipment created successfully',
            'data': output_serializer.data
        }, status=status.HTTP_201_CREATED)
class ShipmentDetails(generics.RetrieveDestroyAPIView): # دالة عرض بيانات تفصيلية عن شحنة
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializerDetail
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return Response({
            'status': 'success',
            'message': 'Shipment details retrieved successfully',
            'data': response.data
        })
    
    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        return Response({   
            'status': 'success',
            'message': 'Shipment deleted successfully',
            'data': response.data
        })
    

    

class ShipmentUpdate(generics.UpdateAPIView):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializerUpdate
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def perform_update(self, serializer):
        user_name = self.request.user.get_full_name() if self.request.user else "مستخدم غير معروف"
        old_instance = self.get_object()
        old_status = old_instance.status

        updated_instance = serializer.save()

        # إذا تغيرت الحالة
        if old_status != updated_instance.status:
            ShipmentHistory.objects.create(
                shipment=updated_instance,
                user=self.request.user,
                old_status=old_status,
                new_status=updated_instance.status,
                action=self.request.method,  # 'PUT'
                notes=f"قام {user_name} بتحديث حالة الشحنة من '{old_status}' إلى '{updated_instance.status}'"
            )
    
    def patch(self, request, *args, **kwargs):
        partial = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response({
                'status': 'success',
                'message': 'Shipment updated successfully',
                'data': serializer.data
            })
        else:
            print("Serializer errors:", serializer.errors)
            return Response(serializer.errors, status=400)

class ShipmentUpdateStatus(generics.UpdateAPIView):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentUpdateStatusSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def patch(self, request, *args, **kwargs):
        partial = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response({
                'status': 'success',
                'message': 'Shipment updated successfully',
                'data': serializer.data
            })
        else:
            print("Serializer errors:", serializer.errors)
            return Response(serializer.errors, status=400)

    def perform_update(self, serializer): # for update after save serializer
        user = self.request.user
        user_name = user.get_full_name()
        old_status = serializer.instance.status

        updated_instance = serializer.save()
        new_status = updated_instance.status

        if old_status != new_status:
            ShipmentHistory.objects.create(
                shipment=updated_instance,
                user=user,
                old_status=old_status,
                new_status=new_status,
                action= self.request.method,
                notes=f"تم تغيير الحالة من '{old_status}' إلى '{new_status}' بواسطة {user_name}"
            )


   



 


        

class ShipmentStatusView(generics.ListCreateAPIView):
    queryset = ShipmentStatus.objects.all().order_by('id')
    serializer_class = ShipmentStatusSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['name_ar', 'name_en']
    search_fields = ['name_ar', 'name_en']

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response({
            'status': 'success',
            'message': 'Shipment status retrieved successfully',
            'data': response.data
        })
    
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return Response({
            'status': 'success',
            'message': 'Shipment status created successfully',
            'data': response.data
        })


class ShipmentStatusOptionsView(generics.ListAPIView):
    queryset = ShipmentStatus.objects.all().order_by('-id')
    serializer_class = ShipmentStatusOptionSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response({
            'status': 'success',
            'message': 'Shipment status options retrieved successfully',
            'data': response.data
        })


class ShipmentOptionsView(generics.ListAPIView):
    queryset = Shipment.objects.all().order_by('-id')
    serializer_class = ShipmentOptionSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response({
            'status': 'success',
            'message': 'Shipment options retrieved successfully',
            'data': response.data
        })


class ClientInvoiceNumberOptionsView(generics.ListAPIView):
    queryset = Shipment.objects.all().order_by('-id')
    serializer_class = ClientInvoiceNumberOptionSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response({
            'status': 'success',
            'message': 'Client invoice number options retrieved successfully',
            'data': response.data
        })

