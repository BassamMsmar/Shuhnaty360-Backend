from django.urls import path
from .views import CityViewSet, CityDetail

urlpatterns = [
    path('', CityViewSet.as_view(), name='City-list-create'),
    path('<int:pk>', CityDetail.as_view(), name='City-list-create'),
]