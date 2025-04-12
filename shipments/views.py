from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.utils import timezone


from .models import Shipment, ShipmentHistory, ShipmentStatus
from .serializers import ShipmentSerializer, ShipmentHistorySerializer

# Create your views here.
class ShipmentViewSet(generics.ListCreateAPIView):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['user', 'driver', 'customer_branch', 'customer_invoice_number', 'recipient', 'status']
    search_fields = ['tracking_number']

class ShipmentDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        old_instance = self.get_object()
        old_status = old_instance.status
        
        updated_instance = serializer.save()

        if old_status != updated_instance.status:
            ShipmentHistory.objects.create(
                shipment=updated_instance,
                user=self.request.user,
                status=updated_instance.status,
                updated_at=timezone.now(),
                notes=f"تم تغيير الحالة من {old_status} إلى {updated_instance.status}"
            )
