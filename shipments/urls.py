from django.urls import path
from .views import ShipmentListCreateView, ShipmentDetails

urlpatterns = [
    path('api/', ShipmentListCreateView.as_view(), name='Shipment-list-create'),
    path('api/<int:pk>', ShipmentDetails.as_view(), name='Shipment-detail-create'),
]