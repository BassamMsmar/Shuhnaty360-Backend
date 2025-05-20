from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Recipient
from .serializers import RecipientSerializer

# Create your views here.
class RecipientViewSet(generics.ListCreateAPIView):
    queryset = Recipient.objects.all()
    serializer_class = RecipientSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

class RecipientDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Recipient.objects.all()
    serializer_class = RecipientSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]