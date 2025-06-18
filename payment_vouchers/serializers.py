from rest_framework import serializers
from .models import PaymentVoucher
from shipments.models import Shipment
from django.contrib.auth import get_user_model

User = get_user_model()

class PaymentVoucherCreateSerializer(serializers.ModelSerializer):
    shipment = serializers.PrimaryKeyRelatedField(queryset=Shipment.objects.all(), required=True)
    creator = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = PaymentVoucher
        fields = [
            'id',
            'shipment',
            'note',
            'creator',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def create(self, validated_data):
        shipment_id = self.context['request'].data.get('shipment')
        creator = self.context['request'].user
        
        try:
            shipment = Shipment.objects.get(id=shipment_id)
            payment_voucher = PaymentVoucher.objects.create(
                shipment=shipment,
                creator=creator
            )
            return payment_voucher
        except Shipment.DoesNotExist:
            raise serializers.ValidationError('الشحنة غير موجودة')


class ShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipment
        fields = [
            'id',

        ]
class PaymentVoucherListSerializer(serializers.ModelSerializer):
    shipment = ShipmentSerializer(read_only=True)
    creator = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = PaymentVoucher
        fields = [
            'id',
            'shipment',
            'creator',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class PaymentVoucherUpdateSerializer(serializers.ModelSerializer):
    shipment = serializers.PrimaryKeyRelatedField(queryset=Shipment.objects.all(), required=True)
    creator = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    class Meta:
        model = PaymentVoucher
        fields = [
            'id',
            'shipment',
            'note',
            'creator',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


    def update(self, instance, validated_data):
        instance.shipment = validated_data.get('shipment', instance.shipment)
        instance.note = validated_data.get('note', instance.note)
        instance.creator = validated_data.get('creator', instance.creator)
        instance.save()
        return instance
