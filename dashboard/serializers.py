from rest_framework import serializers
from shipments.models import Shipment

class ShipmentReportView(serializers.ModelSerializer):
    class Meta:
        model = Shipment
        fields = '__all__'
