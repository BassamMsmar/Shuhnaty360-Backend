from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from .views import UsersViewSet, UsersCreateSet, UserDetaliCreateSet, LoginView, LogoutView

app_name = 'accounts'

urlpatterns = [
    
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),    
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('users/', UsersViewSet.as_view(), name='user-list'),
    path('users/create/', UsersCreateSet.as_view(), name='user-create'),
    path('users/<int:pk>/', UserDetaliCreateSet.as_view(), name='user-detail-update-delete'),
    # path('login/', LoginView.as_view(), name='login'),
    # path('logout/', LogoutView.as_view(), name='logout'),
]