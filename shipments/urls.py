from django.urls import path
from .views import ShipmentListCreateView, ShipmentDetails, ShipmentStatus

urlpatterns = [
    path('api/', ShipmentListCreateView.as_view(), name='Shipment-list-create'),
    path('api/<int:pk>', ShipmentDetails.as_view(), name='Shipment-detail-create'),
    path('api/status/', ShipmentStatus.as_view(), name='Shipment-Status'),
]