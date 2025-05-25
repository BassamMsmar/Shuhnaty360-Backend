from django.urls import path
from .views import DriverViewSet, DriverRetrieveUpdateDestroy, TruckTypeViewSet

urlpatterns = [
    path('', DriverViewSet.as_view(), name='Driver-list-create'),
    path('TruckType/', TruckTypeViewSet.as_view(), name='TruckType-list-create'),
    path('<int:pk>', DriverRetrieveUpdateDestroy.as_view(), name='Driver-detail'),
]