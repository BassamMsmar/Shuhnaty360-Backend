from rest_framework import routers
from django.urls import path
from .views import CompanyProfileViewSet, CompanyBranchViewSet

urlpatterns = [
    path('', CompanyProfileViewSet.as_view(), name='CompanyProfile-list-create'),
    path('branch/', CompanyBranchViewSet.as_view(), name='CompanyBranch-list-create'),
]