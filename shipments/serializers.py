from rest_framework import serializers
from .models import Shipment, ShipmentStatus, ShipmentHistory
from django.contrib.auth.models import User
from .models import Driver, Branch, Recipient, City  # حسب أسماء موديلاتك


class ShipmentHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ShipmentHistory
        fields = '__all__'

class ShipmentSerializercreate(serializers.ModelSerializer):
    class Meta:
        model = Shipment
        fields = [
            'user',
            
            'driver', 
            'origin_city',
            'destination_city',

            'loading_date',
            'days_to_arrive',
            'expected_arrival_date',

            'contents',
            'weight',
            'notes',

            'customer_branch',
            'customer_invoice_number',
            'notes_customer',

            'recipient',
            'notes_recipient',
         
            'fare',
            'premium',
            'fare_return',
            'days_stayed',
            'stay_cost',
            'deducted',

            'status',
        ]


class ShipmentSerializerList(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field='username')
    driver = serializers.SlugRelatedField(read_only=True, slug_field='name')
    customer_branch = serializers.SlugRelatedField(read_only=True, slug_field='name')
    recipient = serializers.SlugRelatedField(read_only=True, slug_field='name')
    origin_city = serializers.SlugRelatedField(read_only=True, slug_field='ar_city')
    destination_city  = serializers.SlugRelatedField(read_only=True, slug_field='ar_city')   
    status  = serializers.SlugRelatedField(read_only=True, slug_field='name_ar')
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

class ShipmentSerializerDetail(serializers.ModelSerializer): # to return all fields in detail  and view in drive as id 
    status = serializers.SlugRelatedField(read_only=True, slug_field='name_ar')
    origin_city = serializers.SlugRelatedField(read_only=True, slug_field='ar_city')
    destination_city  = serializers.SlugRelatedField(read_only=True, slug_field='ar_city')
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
            'weight',
            'contents',
            'notes',
            'status',
            'created_at',
            'updated_at',
            'history',
        ]

