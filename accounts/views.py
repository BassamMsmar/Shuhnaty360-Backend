from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework import generics
from .serializers import UsersSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.settings import api_settings
from rest_framework.permissions import IsAdminUser

# Create your views here.

class UsersViewSet(generics.ListCreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UsersSerializer
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return Response({
            'status': 'success',
            'message': 'Successfully retrieved users list',
            'data': response.data
        })

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return Response({
            'status': 'success',
            'message': 'User created successfully',
            'data': response.data
        })

class UserDetaliCreateSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UsersSerializer
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return Response({
            'status': 'success',
            'message': 'User details retrieved successfully',
            'data': response.data
        })

    def put(self, request, *args, **kwargs):
        response = super().put(request, *args, **kwargs)
        return Response({
            'status': 'success',
            'message': 'User updated successfully',
            'data': response.data
        })

    def patch(self, request, *args, **kwargs):
        response = super().patch(request, *args, **kwargs)
        return Response({
            'status': 'success',
            'message': 'User updated successfully',
            'data': response.data
        })

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        return Response({
            'status': 'success',
            'message': 'User deleted successfully'
        })

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            return Response({
                'status': 'success',
                'message': 'Logout successful'
            })
        except TokenError:
            return Response({
                'status': 'error',
                'message': 'Invalid refresh token'
            }, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            # نحصل على refresh token من الطلب
            refresh_token = request.data.get('refresh_token')
            
            # نتحقق من صحة token
            token = RefreshToken(refresh_token)
            
            # نضيف token إلى blacklist
            token.blacklist()
            
            return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)
        except TokenError:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
