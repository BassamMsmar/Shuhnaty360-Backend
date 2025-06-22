from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status, filters
from rest_framework import filters

from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Sum, F, Q, Min, Max
from shipments.models import Shipment
from django.contrib.auth import get_user_model


User = get_user_model()

# Create your views here


class DashboardView(APIView):
    def get(self, request):
        return Response({"message": "Hello, World!"})


class ShipmentReportView(GenericAPIView):
    queryset = Shipment.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = {
        'user': ['exact'],
        'client_branch': ['exact'],
        'status': ['exact'],
        'created_at': ['gte', 'lte', 'exact'],
    }

    def get(self, request):
        # Get base queryset
        queryset = self.get_queryset().select_related('user', 'client_branch', 'status')
        
        # Apply filters using DjangoFilterBackend
        queryset = self.filter_queryset(queryset)
        
        # Group by user, branch, and status
        report = queryset.values(
            'user__id', 'user__username',
            'client_branch__id', 'client_branch__name',
            'status__id', 'status__name_ar'
        ).annotate(
            count=Count('id'),
            total_fare=Sum('fare'),
            total_premium=Sum('premium'),
            total_deducted=Sum('deducted'),
            total_stay_cost=Sum('stay_cost')
        ).order_by('user__username', 'client_branch__name', 'status__name_ar')
        
        # Get first and last shipment dates
        date_range = queryset.aggregate(
            first_date=Min('created_at'),
            last_date=Max('created_at')
        )
        
        # Initialize result structure
        result = {
            'المستخدمين': {},
            'فروع الشركة': {},
            'التواريخ': {
                'من': date_range['first_date'].strftime('%Y-%m-%d') if date_range['first_date'] else None,
                'إلى': date_range['last_date'].strftime('%Y-%m-%d') if date_range['last_date'] else None
            }
        }
        
        # Calculate shipment counts per user, branch, and status
        user_counts = {}
        branch_counts = {}
        status_counts = {}
        
        for item in report:
            # User counts
            user_key = item['user__username']
            if user_key not in user_counts:
                user_counts[user_key] = 0
            user_counts[user_key] += item['count']
            
            # Branch counts
            branch_key = item['client_branch__name']
            if branch_key not in branch_counts:
                branch_counts[branch_key] = 0
            branch_counts[branch_key] += item['count']
            
            # Status counts
            status_key = item['status__name_ar']
            if status_key not in status_counts:
                status_counts[status_key] = 0
            status_counts[status_key] += item['count']
        
        # Format the response
        result['المستخدمين'] = user_counts
        result['فروع الشركة'] = branch_counts
        result['الحالات'] = status_counts
        
        return Response({
            'status': 'success',
            'data': result
        }, status=status.HTTP_200_OK)