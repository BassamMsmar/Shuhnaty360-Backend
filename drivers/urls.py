from django.urls import path
from .views import DriverViewSet

urlpatterns = [
    path('driver/', DriverViewSet.as_view(), name='Driver-list-create'),
]