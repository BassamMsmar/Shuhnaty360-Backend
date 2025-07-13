# Create your views here.
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import CompanyProfile, CompanyBranch
from .serializers import CompanyProfileSerializer, CompanyBranchSerializer, CompanyOptionSerializer, CompanyBranchOptionSerializer


class CompanyProfileViewSet(generics.ListAPIView):
    queryset = CompanyProfile.objects.all().order_by('id')
    serializer_class = CompanyProfileSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return Response({
            'status': 'success',
            'message': 'Company profiles retrieved successfully',
            'data': response.data
        })

class CompanyBranchViewSet(generics.ListAPIView):
    queryset = CompanyBranch.objects.all().order_by('id')
    serializer_class = CompanyBranchSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return Response({
            'status': 'success',
            'message': 'Company branches retrieved successfully',
            'data': response.data
        })


class CompanyOptionsView(generics.ListAPIView):
    queryset = CompanyProfile.objects.all().order_by('id')
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = CompanyOptionSerializer



    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return Response({
            'status': 'success',
            'message': 'Companies options retrieved successfully',
            'data': response.data
        })


class CompanyBranchOptionsView(generics.ListAPIView):
    queryset = CompanyBranch.objects.all().order_by('id')
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = CompanyBranchOptionSerializer


    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return Response({
            'status': 'success',
            'message': 'Company branches options retrieved successfully',
            'data': response.data
        })
