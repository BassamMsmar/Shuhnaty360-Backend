from rest_framework import serializers
from .models import PaymentVoucher
from shipments.models import Shipment
from shipments.serializers import ShipmentSerializerDetail

from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'last_name', 'first_name']


class PaymentVoucherListSerializer(serializers.ModelSerializer):
    shipment = serializers.PrimaryKeyRelatedField(read_only=True)
    driver = serializers.SlugField(read_only=True)
    origin_city = serializers.SlugField(read_only=True)
    destination_city = serializers.SlugField(read_only=True)
    client = serializers.SlugField(read_only=True)
    client_branch = serializers.SlugField(read_only=True)
    recipient = serializers.SlugField(read_only=True)
    issuing_branch = serializers.SlugField(read_only=True)
    created_by = serializers.SlugField(read_only=True)
    total_cost = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = PaymentVoucher
        fields = [
            'id',
            'tracking_number',
            'shipment',
            'driver',
            'tracking_number',
            'origin_city',
            'destination_city',
            'client',
            'client_branch',
            'issuing_branch',
            'client_invoice_number',
            'recipient',
            'created_at',
            'created_by',
            'is_approved',
            'total_cost',
        ]
        read_only_fields = ['id', 'created_at', 'total_cost']

    def get_total_cost(self, obj):
        return obj.total_cost

class PaymentVoucherCreateSerializer(serializers.ModelSerializer):
    shipment = serializers.PrimaryKeyRelatedField(queryset=Shipment.objects.all(), required=True)
    issuing_branch = serializers.PrimaryKeyRelatedField(read_only=True)
    total_cost = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)


    class Meta:
        model = PaymentVoucher
        fields = [
            'id',
            'shipment',
            'driver',
            'tracking_number',
            'origin_city',
            'destination_city',
            'client',
            'client_branch',
            'issuing_branch',
            'client_invoice_number',
            'recipient',
            'created_at',
            'created_by',
            'is_approved',
            'receiver_name',
            'approved_by',
            'fare',
            'premium',
            'deducted',
            'days_stayed',
            'stay_cost',
            'fare_return',
            'total_cost',
        ]
        read_only_fields = ['id', 'created_at', 'issuing_branch', 'total_cost']
    
    def get_total_cost(self, obj):
        return obj.total_cost

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        
        
        
        if hasattr(self.context['request'].user, 'company_branch'):
            validated_data['issuing_branch'] = self.context['request'].user.company_branch
        
        return super().create(validated_data)
 

class PaymentVoucherDetailSerializer(serializers.ModelSerializer):
    shipment = ShipmentSerializerDetail(read_only=True)
    created_by = serializers.SlugField(read_only=True)
    receiver_name = serializers.SlugField(read_only=True)
    approved_by = serializers.SlugField(read_only=True)
    total_cost = serializers.IntegerField(read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    class Meta:
        model = PaymentVoucher
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']




# ------------------------------
# Option Serializers for Select Fields
# ------------------------------

class PaymentVoucherOptionsSerializer(serializers.ModelSerializer):
    label = serializers.SerializerMethodField()
    value = serializers.IntegerField(source='id')

    class Meta:
        model = PaymentVoucher
        fields = ['value', 'label']
    
    def get_label(self, obj):
        return obj.shipment.id



