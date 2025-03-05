from django.urls import path
from .views import ShipmentViewSet, ShipmentDetails

urlpatterns = [
    path('api/', ShipmentViewSet.as_view(), name='Shipment-list-create'),
    path('api/<int:pk>', ShipmentDetails.as_view(), name='Shipment-detail-create'),
]