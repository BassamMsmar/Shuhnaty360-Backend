from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from django.contrib.auth import get_user_model, login, logout
from rest_framework_simplejwt.authentication import JWTAuthentication


from .serializers import UsersSerializer, UserLoginSerializer, RegisterSerializer

User = get_user_model()

# Create your views here.

class UsersViewSet(generics.ListAPIView):
    queryset = User.objects.all().order_by('id')
    serializer_class = UsersSerializer
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return Response({
            'status': 'success',
            'message': 'Successfully retrieved users list',
            'data': response.data
        })



class UsersCreateSet(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]


    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return Response({
            'status': 'success',
            'message': 'User created successfully',
            'data': response.data
        })


class LoginView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer
    authentication_classes = [JWTAuthentication]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')

        return Response({
            'status': 'success',
            'message': 'Login successful',
            'user_id': user.id,
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'phone': user.phone,
            'company_branch': user.company_branch
        })



class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        logout(request)
        return Response({
            'status': 'success',
            'message': 'Successfully logged out'
        })


class UserDetaliCreateSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UsersSerializer
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]

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

