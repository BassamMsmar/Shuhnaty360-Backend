from rest_framework import serializers
from shipments.models import Shipment

class ShipmentReportView(serializers.ModelSerializer):
    class Meta:
        model = Shipment
        fields = '__all__'

# for swager just not do any think
class ShipmentReportDummySerializer(serializers.Serializer):
    loading_date__gte = serializers.DateField(required=False)
    loading_date__lte = serializers.DateField(required=False)
