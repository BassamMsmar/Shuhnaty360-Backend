from rest_framework import serializers
from .models import CompanyProfile, CompanyBranch

class CompanyProfileSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    class Meta:
        model = CompanyProfile
        fields = '__all__'

class CompanyBranchSerializer(serializers.ModelSerializer): 
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    class Meta:
        model = CompanyBranch
        fields = '__all__'  