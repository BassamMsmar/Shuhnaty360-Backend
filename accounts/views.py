from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import generics

from .models import CustomUser
from .serializers import UsersSerializer

# Create your views here.
class UsersViewSet(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [IsAdminUser]
class UserDetaliCreateSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [IsAdminUser]


