from django.urls import path
from .views import ShipmentListCreateView, ShipmentDetails, ShipmentStatus, ShipmentUpdate

urlpatterns = [
    path('api/', ShipmentListCreateView.as_view(), name='Shipment-list-create'),
    path('api/<int:pk>', ShipmentDetails.as_view(), name='Shipment-detail-create'),
    path('api/status/', ShipmentStatus.as_view(), name='Shipment-Status'),
    path('api/update/<int:pk>', ShipmentUpdate.as_view(), name='Shipment-update'),
]