from django.urls import path
from .views import ClientViewSet

urlpatterns = [
    path('client/', ClientViewSet.as_view(), name='client-list-create'),
]