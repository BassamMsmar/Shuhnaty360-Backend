from django.urls import path
from .views import UsersViewSet, UsersCreateSet, UserDetaliCreateSet, LoginView, LogoutView

app_name = 'accounts'

urlpatterns = [
    path('users/', UsersViewSet.as_view(), name='user-list'),
    path('users/create/', UsersCreateSet.as_view(), name='user-create'),
    path('users/<int:pk>/', UserDetaliCreateSet.as_view(), name='user-detail-update-delete'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]