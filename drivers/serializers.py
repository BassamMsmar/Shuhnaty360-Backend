from rest_framework import serializers
from .models import Driver, TruckType

class DriverSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    class Meta:
        model = Driver
        fields = '__all__'

class TruckTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TruckType
        fields = '__all__'