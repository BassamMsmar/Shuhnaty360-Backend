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

class UserDetaliCreateSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UsersSerializer
    permission_classes = [IsAdminUser]

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

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
