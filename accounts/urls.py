from django.urls import path
from .views import UsersViewSet, UserDetaliCreateSet, RegisterView, LoginView

urlpatterns = [
    path('api/', UsersViewSet.as_view({'get': 'list', 'post': 'create'}), name='user-list-create'),
    path('api/<int:pk>/', UserDetaliCreateSet.as_view(), name='user-detail-update-delete'),
    path('api/register/', RegisterView.as_view({'post': 'create'}), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
]