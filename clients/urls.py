from django.urls import path
from .views import ClientViewSet, ClientDetail

urlpatterns = [
    path('api/', ClientViewSet.as_view(), name='client-list-create'),
    path('api/<int:pk>', ClientDetail.as_view(), name='client-details-create'),
]