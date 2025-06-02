from rest_framework import serializers
from .models import PaymentVoucher
from shipments.serializers import ShipmentSerializerList
from django.contrib.auth import get_user_model

User = get_user_model()

class PaymentVoucherSerializer(serializers.ModelSerializer):
    shipment = ShipmentSerializerList(read_only=True)
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


