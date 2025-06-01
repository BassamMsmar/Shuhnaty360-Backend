from rest_framework import serializers
from .models import Shipment, ShipmentStatus, ShipmentHistory
from django.contrib.auth import get_user_model
from .models import Driver, Branch, Recipient, City, ShipmentStatus  # حسب أسماء موديلاتك

from cities.models import City
from clients.models import Client, Branch   
from drivers.models import Driver , TruckType
from recipient.models import Recipient

User = get_user_model()
class ShipmentStatusSerializer(serializers.ModelSerializer): # Manege shipment status
    class Meta:
        model = ShipmentStatus
        fields = '__all__'

class ShipmentHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ShipmentHistory
        fields = '__all__'

class CitySerializerMini(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'ar_city', 'en_city']

class ClientSerializerMini(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'name']

class BranchSerializerMini(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ['id', 'name']

class DriverSerializerMini(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ['id', 'name']

class RecipientSerializerMini(serializers.ModelSerializer):
    class Meta:
        model = Recipient
        fields = ['id', 'name']

class ShipmentStatusSerializerMini(serializers.ModelSerializer):
    class Meta:
        model = ShipmentStatus
        fields = ['id', 'name_ar', 'name_en']

class UserSerializerMini(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class ShipmentSerializerCreate(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=True)
    driver = serializers.PrimaryKeyRelatedField(queryset=Driver.objects.all(), required=True)
    truck_type = serializers.PrimaryKeyRelatedField(queryset=TruckType.objects.all(), required=True)
    origin_city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all(), required=True)
    destination_city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all(), required=True)
    client = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all(), required=True)
    client_branch = serializers.PrimaryKeyRelatedField(queryset=Branch.objects.all(), required=True)
    recipient = serializers.PrimaryKeyRelatedField(queryset=Recipient.objects.all(), required=True)
    status = serializers.PrimaryKeyRelatedField(queryset=ShipmentStatus.objects.all(), required=True)
    fare = serializers.IntegerField(required=True)
    loading_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    expected_arrival_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    actual_delivery_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    class Meta:
        model = Shipment
        fields = [
            'user',
            
            'driver', 
            'truck_type',
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
    user = UserSerializerMini(read_only=True)
    driver = DriverSerializerMini(read_only=True)
    client = ClientSerializerMini(read_only=True)
    client_branch = BranchSerializerMini(read_only=True)
    recipient = RecipientSerializerMini(read_only=True)
    origin_city = CitySerializerMini(read_only=True)
    destination_city = CitySerializerMini(read_only=True)
    status = ShipmentStatusSerializerMini(read_only=True)    
    def get_fields(self):
        fields = super().get_fields()
        if 'client' in self.context['request'].data:
            client_id = self.context['request'].data['client']
            fields['client_branch'].queryset = Branch.objects.filter(client_id=client_id)
        return fields
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
            'truck_type',
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
    status = ShipmentStatusSerializerMini(read_only=True)
    origin_city = CitySerializerMini(read_only=True)
    destination_city  = CitySerializerMini(read_only=True)
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
            'truck_type',
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
    driver = serializers.PrimaryKeyRelatedField(queryset=Driver.objects.all(), required=True)
    truck_type = serializers.PrimaryKeyRelatedField(queryset=TruckType.objects.all(), required=True)
    origin_city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all(), required=True)
    destination_city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all(), required=True)
    client = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all(), required=True)
    client_branch = serializers.PrimaryKeyRelatedField(queryset=Branch.objects.all(), required=True)
    recipient = serializers.PrimaryKeyRelatedField(queryset=Recipient.objects.all(), required=True)
    status = serializers.PrimaryKeyRelatedField(queryset=ShipmentStatus.objects.all(), required=True)
    fare = serializers.IntegerField(required=True)
    class Meta:
        model = Shipment
        fields = [
    'driver',
    'truck_type',
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