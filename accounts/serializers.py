from rest_framework import serializers
from django.contrib.auth.models import User

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active','is_superuser', 'date_joined']
        read_only_fields = ['id', 'date_joined']