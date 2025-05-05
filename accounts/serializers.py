from rest_framework import serializers
from .models import CustomUser

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'phone',
            'company_branch'
        ]
        read_only_fields = ['id']       