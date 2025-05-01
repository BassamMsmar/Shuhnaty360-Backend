from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import generics

from .models import Driver, TruckType
from .serializers import DriverSerializer, TruckTypeSerializer

# Create your views here.
class DriverViewSet(generics.ListCreateAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    permission_classes = [IsAuthenticated]

class DriverRetrieveUpdateDestroyt(generics.RetrieveUpdateDestroyAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    permission_classes = [IsAuthenticated]

class TruckTypeViewSet(generics.ListCreateAPIView):
    queryset = TruckType.objects.all()
    serializer_class = TruckTypeSerializer
    permission_classes = [IsAuthenticated]
