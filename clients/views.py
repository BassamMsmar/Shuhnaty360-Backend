from typing import override
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import generics

from .models import Client, Branch
from .serializers import ClientSerializer, ClientBranchCreateSerializer, ClientBranchListSerializer

# Create your views here.
class ClientViewSet(generics.ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return Response({
            'status': 'success',
            'message': 'Successfully retrieved clients list',
            'data': response.data
        })

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return Response({
            'status': 'success',
            'message': 'Client created successfully',
            'data': response.data
        })

   

class ClientDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return Response({
            'status': 'success',
            'message': 'Client details retrieved successfully',
            'data': response.data
        })
    
    def put(self, request, *args, **kwargs):
        response = super().put(request, *args, **kwargs)
        return Response({
            'status': 'success',
            'message': 'Client updated successfully',
            'data': response.data
        })
    
    def patch(self, request, *args, **kwargs):
        response = super().patch(request, *args, **kwargs)
        return Response({
            'status': 'success',
            'message': 'Client updated successfully',
            'data': response.data
        })
    
    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        return Response({
            'status': 'success',
            'message': 'Client deleted successfully'
        })

class ClientBranchList(generics.ListAPIView):
    queryset = Branch.objects.all()
    serializer_class = ClientBranchListSerializer
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return Response({
            'status': 'success',
            'message': 'Successfully retrieved branches list',
            'data': response.data
        })
class ClientBranchCreate(generics.CreateAPIView):
    queryset = Branch.objects.all()
    serializer_class = ClientBranchCreateSerializer
    permission_classes = [IsAdminUser]

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return Response({
            'status': 'success',
            'message': 'Branch created successfully',
            'data': response.data
        })

class ClientBranchSDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Branch.objects.all()
    serializer_class = ClientBranchListSerializer
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return Response({
            'status': 'success',
            'message': 'Branch details retrieved successfully',
            'data': response.data
        })
    
    def put(self, request, *args, **kwargs):
        response = super().put(request, *args, **kwargs)
        return Response({
            'status': 'success',
            'message': 'Branch updated successfully',
            'data': response.data
        })
    
    def patch(self, request, *args, **kwargs):
        response = super().patch(request, *args, **kwargs)
        return Response({
            'status': 'success',
            'message': 'Branch updated successfully',
            'data': response.data
        })
    
    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        return Response({
            'status': 'success',
            'message': 'Branch deleted successfully'
        })  