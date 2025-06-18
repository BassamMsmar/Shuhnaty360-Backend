from django.urls import path

from rest_framework_simplejwt.views import TokenVerifyView

from .views import UsersViewSet, UsersCreateSet, UserDetaliCreateSet, UserUpdateSet, CustomTokenObtainPairView, CustomTokenRefreshView, UsersOptionsView

app_name = 'accounts'

urlpatterns = [
    
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),    
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('users/', UsersViewSet.as_view(), name='user-list'),
    path('users/create/', UsersCreateSet.as_view(), name='user-create'),
    path('users/<int:pk>/', UserDetaliCreateSet.as_view(), name='user-detail-update-delete'),
    path('users/<int:pk>/update', UserUpdateSet.as_view(), name='user-update'),
    path('users/options/', UsersOptionsView.as_view(), name='user-options'),
   
]   