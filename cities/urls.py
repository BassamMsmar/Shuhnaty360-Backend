from django.urls import path
from .views import CityViewSet, CityDetail

urlpatterns = [
    path('api/', CityViewSet.as_view(), name='City-list-create'),
    path('api/<int:pk>', CityDetail.as_view(), name='City-list-create'),
]