from django.urls import path
from .views import DriverViewSet, DriverRetrieveUpdateDestroyt

urlpatterns = [
    path('api/', DriverViewSet.as_view(), name='Driver-list-create'),
    path('api/<int:pk>', DriverRetrieveUpdateDestroyt.as_view(), name='Driver-detail'),
]