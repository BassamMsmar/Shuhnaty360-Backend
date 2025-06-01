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

    def validate(self, attrs):
        """Validate user credentials."""
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(
                request=self.context.get('request'),
                username=username,
                password=password
            )
            
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, 
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        write_only=True, 
        required=True,
        style={'input_type': 'password'}
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2', 'first_name', 'last_name', 'phone', 'company_branch', 'is_staff', 'is_superuser')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': False},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone=validated_data.get('phone', ''),
            company_branch=validated_data.get('company_branch', ''),
            is_staff=validated_data.get('is_staff', False),
            is_superuser=validated_data.get('is_superuser', False)
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class CompanyBranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyBranch
        fields = ['id', 'branch_name_ar', 'branch_name_en']
        ref_name = "AccountsCompanyBranch"
class UsersSerializer(serializers.ModelSerializer):
    company_branch = CompanyBranchSerializer()
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined', 'phone', 'company_branch', 'is_superuser',]
        read_only_fields = ['id', 'date_joined']
      