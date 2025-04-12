from rest_framework import serializers
from .models import Shipment, ShipmentStatus, ShipmentHistory
from django.contrib.auth.models import User
from .models import Driver, Branch, Recipient, City  # حسب أسماء موديلاتك


class ShipmentHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ShipmentHistory
        fields = '__all__'


class ShipmentSerializer(serializers.ModelSerializer):
    history = ShipmentHistorySerializer(many=True, read_only=True)
    expected_arrival_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    actual_delivery_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    class Meta:
        model = Shipment
        fields = [
            'id',
            'tracking_number',
            'user',
            'driver',
            'customer_branch',
            'customer_invoice_number',
            'recipient',
            'origin_city',
            'destination_city',
            'fare',
            'premium',
            'fare_return',
            'days_stayed',
            'stay_cost',
            'deducted',
            'days_to_arrive',
            'expected_arrival_date',
            'actual_delivery_date',
            'notes',
            'status',
            'created_at',
            'updated_at',
            'history',
        ]

