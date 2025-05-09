from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined', 'phone', 'company_branch']
        read_only_fields = ['id', 'date_joined']