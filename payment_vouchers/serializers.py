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
    created_by = UserSerializer(read_only=True)
    total_cost = serializers.SerializerMethodField()
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = PaymentVoucher
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_total_cost(self, obj):
        return obj.total_cost

class PaymentVoucherCreateSerializer(serializers.ModelSerializer):
    shipment = serializers.PrimaryKeyRelatedField(queryset=Shipment.objects.all(), required=True)
    total_cost = serializers.SerializerMethodField()
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)


    class Meta:
        model = PaymentVoucher
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_total_cost(self, obj):
        return obj.total_cost

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)

class ShipmentSerializerDetail(serializers.ModelSerializer):
    class Meta:
        model = Shipment
        fields = '__all__'
        

class PaymentVoucherDetailSerializer(serializers.ModelSerializer):
    shipment = ShipmentSerializerDetail(read_only=True)
    created_by = UserSerializer(read_only=True)
    total_cost = serializers.ReadOnlyField()
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    class Meta:
        model = PaymentVoucher
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class PaymentVoucherUpdateSerializer(serializers.ModelSerializer):
    shipment = serializers.PrimaryKeyRelatedField(queryset=Shipment.objects.all(), required=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    class Meta:
        model = PaymentVoucher
        fields = [
            'id',
            'shipment',
            'origin_city',
            'destination_city',
            'client',
            'client_branch',
            'client_invoice_number',
            'recipient',
            'actual_delivery_date',
            'note',
            'fare',
            'premium',
            'fare_return',
            'days_stayed',
            'stay_cost',
            'deducted',
            'updated_at',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

