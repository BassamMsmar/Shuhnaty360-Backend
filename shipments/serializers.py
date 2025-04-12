from rest_framework import serializers
from .models import Shipment, ShipmentStatus
from django.contrib.auth.models import User
from .models import Driver, Branch, Recipient, City  # حسب أسماء موديلاتك

class ShipmentSerializer(serializers.ModelSerializer):
    # user = serializers.SlugRelatedField(
    #     slug_field='username',
    #     queryset=User.objects.all()
    # )
    # driver = serializers.SlugRelatedField(
    #     slug_field='name',
    #     queryset=Driver.objects.all()
    # )
    # customer_branch = serializers.SlugRelatedField(
    #     slug_field='name',
    #     queryset=Branch.objects.all()
    # )
    # recipient = serializers.SlugRelatedField(
    #     slug_field='name',
    #     queryset=Recipient.objects.all()
    # )
    # origin_city = serializers.SlugRelatedField(
    #     slug_field='ar_city',
    #     queryset=City.objects.all()
    # )
    # destination_city = serializers.SlugRelatedField(
    #     slug_field='ar_city',
    #     queryset=City.objects.all()
    # )
    # status = serializers.SlugRelatedField(
    #     slug_field='name_ar',
    #     queryset=ShipmentStatus.objects.all()
    # )
    
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
            'updated_at'
        ]
