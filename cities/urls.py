from django.urls import path
from .views import CityViewSet

urlpatterns = [
    path('city/', CityViewSet.as_view(), name='City-list-create'),
]