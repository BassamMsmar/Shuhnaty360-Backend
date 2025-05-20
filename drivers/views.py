from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Driver, TruckType
from .serializers import DriverSerializer, TruckTypeSerializer

# Create your views here.
class DriverViewSet(generics.ListCreateAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return Response({
            'status': 'success',
            'message': 'Successfully retrieved drivers list',
            'data': response.data
        })

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return Response({
            'status': 'success',
            'message': 'Driver created successfully',
            'data': response.data
        })



class DriverRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return Response({
            'status': 'success',
            'message': 'Driver details retrieved successfully',
            'data': response.data
        })

    def put(self, request, *args, **kwargs):
        response = super().put(request, *args, **kwargs)
        return Response({
            'status': 'success',
            'message': 'Driver updated successfully',
            'data': response.data
        })

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        return Response({
            'status': 'success',
            'message': 'Driver deleted successfully',
            'data': response.data
        })

class TruckTypeViewSet(generics.ListCreateAPIView):
    queryset = TruckType.objects.all()
    serializer_class = TruckTypeSerializer
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]

    

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return Response({
            'status': 'success',
            'message': 'Successfully retrieved truck types list',
            'data': response.data
        })

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return Response({
            'status': 'success',
            'message': 'Truck type created successfully',
            'data': response.data
        })
