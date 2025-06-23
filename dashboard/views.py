from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAdminUser
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from django.db.models import Count, Sum, F, Q, Min, Max


from django.contrib.auth import get_user_model

from shipments.models import Shipment, ShipmentStatus
from profile_company.models import CompanyBranch
from drivers.models import Driver
from clients.models import Client
from recipient.models import Recipient
from cities.models import City



User = get_user_model()


class ShipmentReportView(GenericAPIView):
    queryset = Shipment.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'loading_date': ['gte', 'lte', 'exact'], 
    }

    def get(self, request):
        # Get the base queryset
        queryset = self.filter_queryset(self.get_queryset())
        
        # Get filtered counts
        all_shipments = queryset.count()
        
        # Get branch and status counts from the filtered queryset
        shipment_by_branch = {
            branch.branch_name_ar: queryset.filter(user__company_branch=branch).count()
            for branch in CompanyBranch.objects.all()
        }

        shipment_by_user ={
            user.get_full_name(): queryset.filter(user=user).count()
            for user in User.objects.all()
        }

        shipment_by_status = {
            status.name_ar: queryset.filter(status=status).count()
            for status in ShipmentStatus.objects.all()
        }

        # Get date range info from the filtered queryset
        date_range = queryset.aggregate(
            first_date=Min('loading_date'),
            last_date=Max('loading_date'),
            total_shipments=Count('id'),
        )

        # Format dates for response
        from_date = date_range['first_date'].strftime('%Y-%m-%d') if date_range['first_date'] else None
        to_date = date_range['last_date'].strftime('%Y-%m-%d') if date_range['last_date'] else None

        return Response({
            'all_shipments': all_shipments,
            'shipment_by_branch': shipment_by_branch,
            'shipment_by_status': shipment_by_status,
            'shipment_by_user': shipment_by_user,
            'from_date': from_date,
            'to_date': to_date,
            'total_shipments_in_range': date_range['total_shipments'],
            'applied_filters': {
                'loading_date_gte': request.query_params.get('loading_date__gte'),
                'loading_date_lte': request.query_params.get('loading_date__lte')
            }
        })
