from django.urls import path
from .views import ClientViewSet, ClientDetail, ClientBranchList, ClientBranchCreate, ClientBranchSDetail, ClientBranchUpdate, ClientOptionsView, ClientBranchOptionsView

urlpatterns = [
    path('', ClientViewSet.as_view(), name='client-list-create'),
    path('<int:pk>', ClientDetail.as_view(), name='client-details-create'),
    path('branch/', ClientBranchList.as_view(), name='client-branch-details-create'),
    path('branch/<int:pk>', ClientBranchSDetail.as_view(), name='client-branch-details-create'),
    path('branch/update/<int:pk>', ClientBranchUpdate.as_view(), name='client-branch-update'),
    path('branch/create', ClientBranchCreate.as_view(), name='client-branch-create'),
    path('options/', ClientOptionsView.as_view(), name='client-options'),
    path('branch/options/', ClientBranchOptionsView.as_view(), name='client-branch-options'),
]