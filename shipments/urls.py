from django.urls import path
from .views import ShipmentListView, ShipmentDetails, ShipmentStatus, ShipmentUpdate, ShipmentCreateView

urlpatterns = [
    path('api/', ShipmentListView.as_view(), name='Shipment-list-create'),
    path('api/create/', ShipmentCreateView.as_view(), name='Shipment-create'),
    path('api/<int:pk>', ShipmentDetails.as_view(), name='Shipment-detail-create'),
    path('api/status/', ShipmentStatus.as_view(), name='Shipment-Status'),
    path('api/update/<int:pk>', ShipmentUpdate.as_view(), name='Shipment-update'),
]