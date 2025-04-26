from django.urls import path
from .views import DriverViewSet, DriverRetrieveUpdateDestroyt, TruckTypeViewSet

urlpatterns = [
    path('api/', DriverViewSet.as_view(), name='Driver-list-create'),
    path('api/TruckType/', TruckTypeViewSet.as_view(), name='TruckType-list-create'),
    path('api/<int:pk>', DriverRetrieveUpdateDestroyt.as_view(), name='Driver-detail'),
]