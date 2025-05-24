from rest_framework import serializers
from .models import CompanyProfile, CompanyBranch


class CompanyBranchSerializer(serializers.ModelSerializer): 
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    ref_name = "ProfileCompanyBranch"
    class Meta:
        model = CompanyBranch
        fields = '__all__'  
class CompanyProfileSerializer(serializers.ModelSerializer):
    branches = CompanyBranchSerializer(many=True, read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    class Meta:
        model = CompanyProfile
        fields = ['id', 'company_name_ar', 'company_name_en', 'company_logo', 'company_description_ar', 'company_description_en', 'main_phone_number', 'secondary_phone_number', 'email', 'website', 'address', 'city', 'branches', 'created_at', 'updated_at']

