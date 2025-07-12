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
    driver = serializers.SlugField()
    origin_city = serializers.SlugField()
    destination_city = serializers.SlugField()
    client = serializers.SlugField()
    receiver_name = serializers.SlugField()
    client_branch = serializers.SlugField()
    recipient = serializers.SlugField()
    issuing_branch = serializers.SlugField()
    created_by = serializers.SlugField()
    reviewed_by = serializers.SlugField()
    approval_status_display = serializers.SerializerMethodField()
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
            'reviewed_by',
            'approval_status',           # القيمة الأصلية (pending, approved, rejected)
            'approval_status_display',   # النص العربي المقروء
            'receiver_name',
            'total_cost',
        ]
        read_only_fields = ['id', 'created_at', 'total_cost']

    def get_total_cost(self, obj):
        return obj.total_cost

    def get_approval_status_display(self, obj):
        return obj.get_approval_status_display()

    def get_reviewed_by(self, obj):
        return obj.reviewed_by.get_full_name() if obj.reviewed_by else None
class PaymentVoucherCreateSerializer(serializers.ModelSerializer):
    shipment = serializers.PrimaryKeyRelatedField(
        queryset=Shipment.objects.all(), required=True
    )
    issuing_branch = serializers.PrimaryKeyRelatedField(read_only=True)
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)
    total_cost = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", read_only=True
    )

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
            'approval_status',
            'receiver_name',
            'fare',
            'premium',
            'deducted',
            'days_stayed',
            'stay_cost',
            'fare_return',
            'total_cost',
        ]
        read_only_fields = ['id', 'created_at', 'issuing_branch', 'created_by', 'total_cost']

    def get_total_cost(self, obj):
        return obj.total_cost

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['created_by'] = request.user
            # تعيين فرع الإصدار إذا كان مرتبط بالمستخدم
            company_branch = getattr(request.user, 'company_branch', None)
            if company_branch:
                validated_data['issuing_branch'] = company_branch
        return super().create(validated_data)
class PaymentVoucherDetailSerializer(serializers.ModelSerializer):
    shipment = ShipmentSerializerDetail(read_only=True)

    created_by = serializers.SlugField()
    receiver_name = serializers.SlugField()
    reviewed_by = serializers.SlugField()

    approval_status_display = serializers.SerializerMethodField()
    total_cost = serializers.SerializerMethodField()

    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = PaymentVoucher
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'total_cost']

    def get_approval_status_display(self, obj):
        return obj.get_approval_status_display()

    def get_total_cost(self, obj):
        return obj.total_cost

    def get_receiver_name(self, obj):
        if obj.receiver_name:
            return obj.receiver_name.get_full_name()
        return None

    def get_created_by(self, obj):
        if obj.created_by:
            return obj.created_by.get_full_name()
        return None

    def get_reviewed_by(self, obj):
        if obj.reviewed_by:
            return obj.reviewed_by.get_full_name()
        return None

from rest_framework import serializers
from .models import PaymentVoucher


class PaymentVoucherUpdateSerializer(serializers.ModelSerializer):
    approval_status_display = serializers.SerializerMethodField()
    total_cost = serializers.SerializerMethodField()
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = PaymentVoucher
        fields = [
            'id',
            'driver',
            'tracking_number',
            'origin_city',
            'destination_city',
            'client',
            'client_branch',
            'client_invoice_number',
            'recipient',
            'approval_status',
            'rejection_reason',
            'receiver_name',
            'fare',
            'premium',
            'deducted',
            'days_stayed',
            'stay_cost',
            'fare_return',
            'note',
            'created_at',
            'updated_at',
            'total_cost',
            'approval_status_display',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'total_cost', 'approval_status_display']

    def get_total_cost(self, obj):
        return obj.total_cost

    def get_approval_status_display(self, obj):
        return obj.get_approval_status_display()

    def update(self, instance, validated_data):
        request = self.context.get('request')

        # سجل من قام بالمراجعة إذا تم تغيير حالة الموافقة
        if 'approval_status' in validated_data and request and request.user.is_authenticated:
            instance.reviewed_by = request.user

        # تحديث الحقول المسموح بها
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance



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



