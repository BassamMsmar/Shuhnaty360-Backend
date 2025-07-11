from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import filters
from .models import Recipient
from .serializers import RecipientSerializerList, RecipientSerializerCreate, RecipientOptionSerializer

# Create your views here.
class RecipientViewSet(generics.ListAPIView):
    queryset = Recipient.objects.all().order_by('id')
    serializer_class = RecipientSerializerList
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    filter_backends = [filters.SearchFilter]
    search_fields = ['id', 'name']

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return Response({
            'status': 'success',
            'message': 'Successfully retrieved recipients list',
            'data': response.data
        })
class RecipientCreateView(generics.CreateAPIView):
    queryset = Recipient.objects.all()
    serializer_class = RecipientSerializerCreate
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def perform_create(self, serializer):
        serializer.save()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        output_serializer = RecipientSerializerList(serializer.instance, context={'request': request})
        return Response({
            'status': 'success',
            'message': 'Successfully created recipient',
            'data': output_serializer.data
        }, status=status.HTTP_201_CREATED)

class RecipientDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Recipient.objects.all()
    serializer_class = RecipientSerializerCreate
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return Response({
            'status': 'success',
            'message': 'Successfully retrieved recipient details',
            'data': response.data
        })

    def put(self, request, *args, **kwargs):
        response = super().put(request, *args, **kwargs)
        return Response({
            'status': 'success',
            'message': 'Successfully updated recipient',
            'data': response.data
        })

    def patch(self, request, *args, **kwargs):
        return self.put(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return Response({
            'status': 'success',
            'message': 'Successfully deleted recipient'
        }, status=status.HTTP_204_NO_CONTENT)


class RecipientOptionsView(generics.ListAPIView):
    queryset = Recipient.objects.all()
    serializer_class = RecipientOptionSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]


    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return Response({
            'status': 'success',
            'message': 'Recipients options retrieved successfully',
            'data': response.data
        })
