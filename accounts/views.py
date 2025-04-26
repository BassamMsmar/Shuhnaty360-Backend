from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import generics

from django.contrib.auth.models import User
from .serializers import UsersSerializer

# Create your views here.
class UsersViewSet(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [IsAdminUser]
class UserDetaliCreateSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [IsAdminUser]


