from django.urls import path
from .views import DashboardView

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
]
from django.urls import path
from .views import DashboardView, ShipmentReportView    

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('shipments/report/', ShipmentReportView.as_view(), name='shipment-report'),
]
