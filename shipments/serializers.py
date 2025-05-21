from rest_framework import serializers
from .models import Shipment, ShipmentStatus, ShipmentHistory
from django.contrib.auth import get_user_model
from .models import Driver, Branch, Recipient, City, ShipmentStatus  # حسب أسماء موديلاتك

User = get_user_model()
class ShipmentStatusSerializer(serializers.ModelSerializer): # Manege shipment status
    class Meta:
        model = ShipmentStatus
        fields = '__all__'

class ShipmentHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ShipmentHistory
        fields = '__all__'

class ShipmentSerializerCreate(serializers.ModelSerializer):
    loading_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    expected_arrival_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    actual_delivery_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
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
            'actual_delivery_date',

            'contents',
            'weight',
            'notes',

            'client',
            'client_branch',
            'client_invoice_number',
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
    total_cost = serializers.ReadOnlyField()
    user = serializers.SlugRelatedField(read_only=True, slug_field='username')
    driver = serializers.SlugRelatedField(read_only=True, slug_field='name')
    client = serializers.SlugRelatedField(read_only=True, slug_field='name')
    
    def get_fields(self):
        fields = super().get_fields()
        if 'client' in self.context['request'].data:
            client_id = self.context['request'].data['client']
            fields['client_branch'].queryset = Branch.objects.filter(client_id=client_id)
        return fields
    
    client_branch = serializers.SlugRelatedField(
        queryset=Branch.objects.all(),
        slug_field='name'
    )
    recipient = serializers.SlugRelatedField(read_only=True, slug_field='name')
    origin_city = serializers.SlugRelatedField(read_only=True, slug_field='ar_city')
    destination_city  = serializers.SlugRelatedField(read_only=True, slug_field='ar_city')   
    status  = serializers.SlugRelatedField(read_only=True, slug_field='name_ar')
    history = ShipmentHistorySerializer(many=True, read_only=True)
    expected_arrival_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    actual_delivery_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    loading_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    class Meta:
        model = Shipment
        fields = [
            'id',
            'tracking_number',
            'user',
            'driver',
            'client',
            'client_branch',
            'client_invoice_number',
            'notes_customer',
            'recipient',
            'notes_recipient',
            'origin_city',
            'destination_city',
            'fare',
            'premium',
            'fare_return',
            'days_stayed',
            'stay_cost',
            'deducted',
            'total_cost',
            'days_to_arrive',
            'expected_arrival_date',
            'actual_delivery_date',
            'notes',
            'weight',
            'contents',
            'status',
            'loading_date',
            'updated_at',
            'history',
        ]

class ShipmentSerializerDetail(serializers.ModelSerializer):
    total_cost = serializers.ReadOnlyField() # to return all fields in detail  and view in drive as id 
    status = serializers.SlugRelatedField(read_only=True, slug_field='name_ar')
    origin_city = serializers.SlugRelatedField(read_only=True, slug_field='ar_city')
    destination_city  = serializers.SlugRelatedField(read_only=True, slug_field='ar_city')
    history = ShipmentHistorySerializer(many=True, read_only=True)
    expected_arrival_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    actual_delivery_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    loading_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    class Meta:
        model = Shipment
        fields = [
            'id',
            'tracking_number',
            'user',
            'driver',
            'client',
            'client_branch',
            'client_invoice_number',
            'recipient',
            'origin_city',
            'destination_city',
            'fare',
            'premium',
            'fare_return',
            'days_stayed',
            'stay_cost',
            'deducted',
            'total_cost',
            'days_to_arrive',
            'expected_arrival_date',
            'actual_delivery_date',
            'weight',
            'contents',
            'notes',
            'status',
            'loading_date',
            'updated_at',
            'history',
        ]

class ShipmentSerializerUpdate(serializers.ModelSerializer):
    class Meta:
        model = Shipment
        fields = [
    'driver',
    'client_invoice_number',
    'client',
    'client_branch',
    'recipient',
    'status',
    'origin_city',
    'destination_city',
    'days_to_arrive',
    'loading_date',
    'days_stayed',
    'actual_delivery_date',
    'expected_arrival_date',
    'notes',
    'notes_customer',
    'notes_recipient',
    'fare_return',
    'deducted',
    'stay_cost',
    'weight',
    'contents',
    'fare',
    'premium',
    'total_cost',
        ]
