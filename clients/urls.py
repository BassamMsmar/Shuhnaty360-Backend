from django.urls import path
from .views import ClientViewSet, ClientBranchSDetail, ClientBranchS, ClientDetail

urlpatterns = [
    path('api/', ClientViewSet.as_view(), name='client-list-create'),
    path('api/<int:pk>', ClientDetail.as_view(), name='client-details-create'),
    path('api/branch/', ClientBranchS.as_view(), name='client-branch-details-create'),
    path('api/branch/<int:pk>', ClientBranchSDetail.as_view(), name='client-branch-details-create'),
]