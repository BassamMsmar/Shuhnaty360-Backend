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
    created_by = serializers.SlugField(read_only=True)
    receiver_name = serializers.SlugField(read_only=True)
    approved_by = serializers.SlugField(read_only=True)
    total_cost = serializers.SerializerMethodField()
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
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
            'client_invoice_number',
            'recipient',
            'created_at',
            'created_by',
            'is_approved',
            'receiver_name',
            'approved_by',
            'updated_at',
            'total_cost',
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
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_total_cost(self, obj):
        return obj.total_cost

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)
 

class PaymentVoucherDetailSerializer(serializers.ModelSerializer):
    shipment = ShipmentSerializerDetail(read_only=True)
    created_by = serializers.SlugField(read_only=True)
    receiver_name = serializers.SlugField(read_only=True)
    approved_by = serializers.SlugField(read_only=True)
    total_cost = serializers.ReadOnlyField()
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    class Meta:
        model = PaymentVoucher
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'total_cost']

class PaymentVoucherUpdateSerializer(serializers.ModelSerializer):
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
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
            'created_at',
            'is_approved',
            'receiver_name',
            'approved_by',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


    def update(self, instance, validated_data):
        request = self.context['request']
        is_approved = validated_data.get('is_approved', instance.is_approved)

        # إذا تم تعيين الموافقة لأول مرة
        if is_approved and not instance.approved_by:
            validated_data['approved_by'] = request.user

        return super().update(instance, validated_data)








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



