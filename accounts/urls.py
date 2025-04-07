from django.urls import path
from .views import UsersViewSet

urlpatterns = [
    path('api/', UsersViewSet.as_view(), name='user-list-create'),
]