from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import generics

from .models import Client, Branch
from .serializers import ClientSerializer, ClientBranchSerializer

# Create your views here.
class ClientViewSet(generics.ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAdminUser]

class ClientDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAdminUser]


class ClientBranchS(generics.ListCreateAPIView):
    queryset = Branch.objects.all()
    serializer_class = ClientBranchSerializer
    permission_classes = [IsAdminUser]

class ClientBranchSDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Branch.objects.all()
    serializer_class = ClientBranchSerializer
    permission_classes = [IsAdminUser]