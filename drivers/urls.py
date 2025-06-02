from django.urls import path
from .views import DriverListViewSet, TruckTypeViewSet, DriverCreateViewSet ,DriverRetrieve, DriverUpdate

urlpatterns = [
    path('', DriverListViewSet.as_view(), name='Driver-list'),
    path('create/', DriverCreateViewSet.as_view(), name='Driver-create'),
    path('TruckType/', TruckTypeViewSet.as_view(), name='TruckType-list-create'),
    path('<int:pk>', DriverRetrieve.as_view(), name='Driver-detail'),
    path('update/<int:pk>', DriverUpdate.as_view(), name='Driver-detail'),
]