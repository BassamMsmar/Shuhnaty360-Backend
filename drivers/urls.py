from django.urls import path
from .views import DriverListViewSet, TruckTypeViewSet, DriverCreateViewSet ,DriverRetrieve, DriverUpdate, DriverOptionsView, TruckTypeOptionsView

urlpatterns = [
    path('', DriverListViewSet.as_view(), name='Driver-list'),
    path('create/', DriverCreateViewSet.as_view(), name='Driver-create'),
    path('TruckType/', TruckTypeViewSet.as_view(), name='TruckType-list-create'),
    path('<int:pk>', DriverRetrieve.as_view(), name='Driver-detail'),
    path('update/<int:pk>', DriverUpdate.as_view(), name='Driver-detail'),
    path('options/', DriverOptionsView.as_view(), name='Driver-options'),
    path('TruckType/options/', TruckTypeOptionsView.as_view(), name='TruckType-options'),
]