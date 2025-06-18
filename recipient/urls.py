from django.urls import path
from .views import RecipientViewSet, RecipientDetails, RecipientCreateView, RecipientOptionsView

urlpatterns = [
    path('', RecipientViewSet.as_view(), name='Recipient-list-create'),
    path('create/', RecipientCreateView.as_view(), name='Recipient-create'),
    path('<int:pk>', RecipientDetails.as_view(), name='Recipient-details-create'),
    path('options/', RecipientOptionsView.as_view(), name='Recipient-options'),
]