from django.urls import path
from .views import RecipientViewSet

urlpatterns = [
    path('api/', RecipientViewSet.as_view(), name='Recipient-list-create'),
]