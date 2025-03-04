from django.urls import path
from .views import CityViewSet

urlpatterns = [
    path('api/', CityViewSet.as_view(), name='City-list-create'),
]