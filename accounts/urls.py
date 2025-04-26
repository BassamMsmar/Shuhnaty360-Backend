from django.urls import path
from .views import UsersViewSet,UserDetaliCreateSet

urlpatterns = [
    path('api/', UsersViewSet.as_view(), name='user-list-create'),
    path('api/<int:pk>/', UserDetaliCreateSet.as_view(), name='user-detail-update-delete'),
    
]