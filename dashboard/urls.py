from django.urls import path
from .views import ShipmentReportView

urlpatterns = [
    path('shipment-report/', ShipmentReportView.as_view(), name='shipment-report'),
]
