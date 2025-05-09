from django.urls import path
from .views import UsersViewSet, UserDetaliCreateSet, LogoutView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

app_name = 'accounts'

urlpatterns = [
    path('users/', UsersViewSet.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserDetaliCreateSet.as_view(), name='user-detail-update-delete'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh-token/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verify-token/', TokenVerifyView.as_view(), name='token_verify'),
]