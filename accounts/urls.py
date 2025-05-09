from django.urls import path
from .views import UsersViewSet, UserDetaliCreateSet

app_name = 'accounts'

urlpatterns = [
    path('users/', UsersViewSet.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserDetaliCreateSet.as_view(), name='user-detail-update-delete'),
]