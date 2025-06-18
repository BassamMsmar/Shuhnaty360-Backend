from rest_framework import routers
from django.urls import path
from .views import CompanyProfileViewSet, CompanyBranchViewSet, CompanyOptionsView, CompanyBranchOptionsView

urlpatterns = [
    path('', CompanyProfileViewSet.as_view(), name='CompanyProfile-list-create'),
    path('branch/', CompanyBranchViewSet.as_view(), name='CompanyBranch-list-create'),

    path('companies/', CompanyOptionsView.as_view(), name='company-list'),
    path('companies/options/', CompanyOptionsView.as_view(), name='company-options'),
    path('company-branches/', CompanyBranchOptionsView.as_view(), name='company-branch-list'),
    path('company-branches/options/', CompanyBranchOptionsView.as_view(), name='company-branch-options'),
]