from django.urls import path
from .views import ShipmentViewSet

urlpatterns = [
    path('shipment/', ShipmentViewSet.as_view(), name='Shipment-list-create'),
]