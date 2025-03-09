from rest_framework import serializers
from .models import Shipment

class ShipmentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    driver = serializers.SerializerMethodField()
    customer_branch = serializers.SerializerMethodField()
    recipient = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    origin_city = serializers.SerializerMethodField()
    destination_city = serializers.SerializerMethodField()
    client = serializers.SerializerMethodField()
    branch = serializers.SerializerMethodField()




    class Meta:
        model = Shipment
        fields = ['id', 'user', 'driver', 'customer_branch', 'customer_invoice_number', 'recipient', 'fare', 'premium', 'fare_return', 'origin_city', 'destination_city', 'status', 'client', 'branch']
    
    def get_user(self, obj):
        return obj.user.username
    
    def get_driver(self, obj):
        return obj.driver.name
    
    def get_customer_branch(self, obj):
        return obj.customer_branch.name
    
    def get_recipient(self, obj):
        return obj.recipient.name
    
    def get_status(self, obj):
        return obj.status.name_en
    
    def get_origin_city(self, obj):
        return obj.origin_city.en_city
    
    def get_destination_city(self, obj):
        return obj.destination_city.en_city
    
    def get_client(self, obj):
        return obj.customer_branch.client.name
    
    def get_branch(self, obj):
        return obj.customer_branch.name
    
