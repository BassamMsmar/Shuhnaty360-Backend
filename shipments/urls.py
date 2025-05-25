from django.urls import path
from .views import ShipmentListView, ShipmentDetails, ShipmentStatus, ShipmentUpdate, ShipmentCreateView

urlpatterns = [
    path('', ShipmentListView.as_view(), name='Shipment-list-create'),
    path('create/', ShipmentCreateView.as_view(), name='Shipment-create'),
    path('<int:pk>', ShipmentDetails.as_view(), name='Shipment-detail-create'),
    path('status/', ShipmentStatus.as_view(), name='Shipment-Status'),
    path('update/<int:pk>', ShipmentUpdate.as_view(), name='Shipment-update'),
]