from django.urls import path
from .views import RecipientViewSet, RecipientDetails, RecipientCreateView

urlpatterns = [
    path('api/', RecipientViewSet.as_view(), name='Recipient-list-create'),
    path('api/create/', RecipientCreateView.as_view(), name='Recipient-create'),
    path('api/<int:pk>', RecipientDetails.as_view(), name='Recipient-details-create'),
]