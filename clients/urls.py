from django.urls import path
from .views import ClientViewSet, ClientDetail, ClientBranchList, ClientBranchCreate, ClientBranchSDetail

urlpatterns = [
    path('api/', ClientViewSet.as_view(), name='client-list-create'),
    path('api/<int:pk>', ClientDetail.as_view(), name='client-details-create'),
    path('api/branch/', ClientBranchList.as_view(), name='client-branch-details-create'),
    path('api/branch/<int:pk>', ClientBranchSDetail.as_view(), name='client-branch-details-create'),
]