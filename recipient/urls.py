from django.urls import path
from .views import RecipientViewSet, RecipientDetails

urlpatterns = [
    path('api/', RecipientViewSet.as_view(), name='Recipient-list-create'),
    path('api/<int:pk>', RecipientDetails.as_view(), name='Recipient-details-create'),
]