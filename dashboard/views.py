from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Count, Sum, F, Q
from shipments.models import Shipment
from django.contrib.auth import get_user_model
from clients.models import Branch

User = get_user_model()

# Create your views here


class DashboardView(APIView):
    def get(self, request):
        return Response({"message": "Hello, World!"})


class ShipmentReportView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get query parameters
        user_id = request.query_params.get('user_id')
        branch_id = request.query_params.get('branch_id')
        status = request.query_params.get('status')
        
        # Start with base queryset
        queryset = Shipment.objects.select_related('user', 'client_branch', 'status')
        
        # Apply filters if provided
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        if branch_id:
            queryset = queryset.filter(client_branch_id=branch_id)
        if status:
            queryset = queryset.filter(status_id=status)
        
        # Group by user, branch, and status
        report = queryset.values(
            'user__id', 'user__username',
            'client_branch__id', 'client_branch__name_ar',
            'status__id', 'status__name_ar'
        ).annotate(
            count=Count('id'),
            total_fare=Sum('fare'),
            total_premium=Sum('premium'),
            total_deducted=Sum('deducted'),
            total_stay_cost=Sum('stay_cost')
        ).order_by('user__username', 'client_branch__name_ar', 'status__name_ar')
        
        # Format the response
        result = {}
        for item in report:
            user_key = f"{item['user__username']} (ID: {item['user__id']})"
            branch_key = f"{item['client_branch__name_ar']} (ID: {item['client_branch__id']})"
            status_key = f"{item['status__name_ar']} (ID: {item['status__id']})"
            
            if user_key not in result:
                result[user_key] = {}
            if branch_key not in result[user_key]:
                result[user_key][branch_key] = {}
                
            result[user_key][branch_key][status_key] = {
                'count': item['count'],
                'total_fare': item['total_fare'] or 0,
                'total_premium': item['total_premium'] or 0,
                'total_deducted': item['total_deducted'] or 0,
                'total_stay_cost': item['total_stay_cost'] or 0,
                'net_total': (item['total_fare'] or 0) + 
                            (item['total_premium'] or 0) - 
                            (item['total_deducted'] or 0) + 
                            (item['total_stay_cost'] or 0)
            }
        
        return Response({
            'status': 'success',
            'data': result
        }, status=status.HTTP_200_OK)