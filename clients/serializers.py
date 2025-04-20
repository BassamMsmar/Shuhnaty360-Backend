from rest_framework import serializers
from .models import Client, Branch

class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = '__all__'

class ClientSerializer(serializers.ModelSerializer):
    branches = BranchSerializer(many=True, read_only=True)
    class Meta:
        model = Client
        fields = ['id', 'name', 'address', 'phone_number','second_phone_number', 'email', 'dicription', 'branches']
