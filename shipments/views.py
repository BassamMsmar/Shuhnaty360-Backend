from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from .models import Shipment
from .serializers import ShipmentSerializer

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