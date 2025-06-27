from django.urls import path
from .views import ShipmentListView, ShipmentDetails, ShipmentStatusView, ShipmentUpdate, ShipmentCreateView, ShipmentOptionsView, ShipmentStatusOptionsView, ClientInvoiceNumberOptionsView

urlpatterns = [
    path('', ShipmentListView.as_view(), name='Shipment-list-create'),
    path('create/', ShipmentCreateView.as_view(), name='Shipment-create'),
    path('<int:pk>', ShipmentDetails.as_view(), name='Shipment-detail-create'),
    path('status/', ShipmentStatusView.as_view(), name='Shipment-Status'),
    path('update/<int:pk>', ShipmentUpdate.as_view(), name='Shipment-update'),
    path('options/', ShipmentOptionsView.as_view(), name='Shipment-options'),
    path('status/options/', ShipmentStatusOptionsView.as_view(), name='Shipment-status-options'),
    path('client/invoice-number/options/', ClientInvoiceNumberOptionsView.as_view(), name='Shipment-client-invoice-number-options'),
]