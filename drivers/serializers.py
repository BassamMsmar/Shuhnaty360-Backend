from rest_framework import serializers
from .models import Driver, TruckType


class TruckTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TruckType
        fields = '__all__'

class DriverListSerializer(serializers.ModelSerializer):
    truck_type = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    class Meta:
        model = Driver
        fields = '__all__'

    def get_truck_type(self, obj):
        return obj.truck_type.name_ar if obj.truck_type else None
class DriverCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = '__all__'


class DriverOptionSerializer(serializers.ModelSerializer):
    label = serializers.SerializerMethodField()
    value = serializers.IntegerField(source='id')

    class Meta:
        model = Driver
        fields = ['value', 'label']

    def get_label(self, obj):
        return obj.name

class TruckTypeOptionSerializer(serializers.ModelSerializer):
    label = serializers.SerializerMethodField()
    value = serializers.IntegerField(source='id')

    class Meta:
        model = TruckType
        fields = ['value', 'label']

    def get_label(self, obj):
        return obj.name_ar