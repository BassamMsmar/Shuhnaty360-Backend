from rest_framework import routers
from django.urls import path
from .views import CompanyProfileViewSet, CompanyBranchViewSet

urlpatterns = [
    path('api/', CompanyProfileViewSet.as_view(), name='CompanyProfile-list-create'),
    path('api/branch/', CompanyBranchViewSet.as_view(), name='CompanyBranch-list-create'),
]