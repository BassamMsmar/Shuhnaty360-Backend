from rest_framework import serializers
from .models import PaymentVoucher
from shipments.models import Shipment
from django.contrib.auth import get_user_model

User = get_user_model()

class ShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipment
        fields = [
            'id',

        ]

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
        fields = [
            'id',
            'shipment',
            'note',
            'updated_at',
            'created_at',
            'created_by',
            'fare',
            'premium',
            'fare_return',
            'days_stayed',
            'stay_cost',
            'deducted',
            'total_cost'
                ]
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
        fields = [
            'id',
            'shipment',
            'note',
            'updated_at',
            'created_at',
            'fare',
            'premium',
            'fare_return',
            'days_stayed',
            'stay_cost',
            'deducted',
            'total_cost'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_total_cost(self, obj):
        return obj.total_cost

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)

class shipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipment
        fields = ['id'
        , 'tracking_number'
        , 'fare'
        , 'premium'
        , 'fare_return'
        , 'days_stayed'
        , 'stay_cost'
        , 'deducted'
        , 'total_cost'
        , 'user'
        , 'driver'
        , 'client'
        , 'client_branch'
        , 'client_invoice_number'
        , 'recipient'
        , 'origin_city'
        , 'destination_city'
        , 'loading_date'
        , 'days_to_arrive'
        , 'expected_arrival_date'
        , 'actual_delivery_date'
        , 'weight'
        , 'contents'
        , 'created_at'
        , 'updated_at'
        ]

class PaymentVoucherDetailSerializer(serializers.ModelSerializer):
    shipment = shipmentSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)
    total_cost = serializers.ReadOnlyField()
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    class Meta:
        model = PaymentVoucher
        fields = [
            'id',
            'shipment',
            'note',
            'created_by',
            'created_at',
            'updated_at',
            'fare',
            'premium',
            'fare_return',
            'days_stayed',
            'stay_cost',
            'deducted',
            'total_cost'    
        ]
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
            'note',
            'created_at',
            'updated_at',
            'fare',
            'premium',
            'fare_return',
            'days_stayed',
            'stay_cost',
            'deducted'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

