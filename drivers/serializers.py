from rest_framework import serializers
from .models import Driver, TruckType


class TruckTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TruckType
        fields = '__all__'

class DriverListSerializer(serializers.ModelSerializer):
    truck_type = serializers.SlugField(source='truck_type.name_ar')
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    class Meta:
        model = Driver
        fields = '__all__'
class DriverCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = '__all__'
