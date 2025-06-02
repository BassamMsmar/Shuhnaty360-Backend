from django.urls import path
from .views import DriverListViewSet, DriverRetrieveUpdateDestroy, TruckTypeViewSet, DriverCreateViewSet 

urlpatterns = [
    path('', DriverListViewSet.as_view(), name='Driver-list'),
    path('create/', DriverCreateViewSet.as_view(), name='Driver-create'),
    path('TruckType/', TruckTypeViewSet.as_view(), name='TruckType-list-create'),
    path('<int:pk>', DriverRetrieveUpdateDestroy.as_view(), name='Driver-detail'),
]