from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import CompanyProfile, CompanyBranch
from .serializers import CompanyProfileSerializer, CompanyBranchSerializer


class CompanyProfileViewSet(generics.ListAPIView):
    queryset = CompanyProfile.objects.all()
    serializer_class = CompanyProfileSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

class CompanyBranchViewSet(generics.ListAPIView):
    queryset = CompanyBranch.objects.all()
    serializer_class = CompanyBranchSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
