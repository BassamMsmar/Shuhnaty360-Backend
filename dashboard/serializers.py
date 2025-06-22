from rest_framework import serializers
from shipments.models import Shipment
from clients.models import Branch

class ShipmentReportView(serializers.ModelSerializer):
    class Meta:
        model = Shipment
        fields = '__all__'

