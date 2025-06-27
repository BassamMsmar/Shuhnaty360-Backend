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
        queryset = self.filter_queryset(self.get_queryset())
        all_shipments = queryset.count()

        statuses = ShipmentStatus.objects.all()

        # توزيع الشحنات حسب الفروع وحالاتها
        shipment_by_branch = {}
        for branch in CompanyBranch.objects.all():
            branch_queryset = queryset.filter(user__company_branch=branch)
            branch_data = {
                "كل الشحنات": branch_queryset.count()
            }
            for status in statuses:
                branch_data[status.name_ar] = branch_queryset.filter(status=status).count()
            shipment_by_branch[branch.branch_name_ar] = branch_data

        # توزيع الشحنات حسب المدن وحالاتها
        shipment_by_city = {}
        for city in City.objects.all():
            city_queryset = queryset.filter(destination_city=city)
            city_data = {
                "كل الشحنات": city_queryset.count()
            }
            for status in statuses:
                city_data[status.name_ar] = city_queryset.filter(status=status).count()
            shipment_by_city[city.ar_city] = city_data

        # توزيع الشحنات حسب المستخدمين وحالاتهم
        shipment_by_user = {}
        for user in User.objects.all():
            user_queryset = queryset.filter(user=user)
            user_data = {
                "كل الشحنات": user_queryset.count()
            }
            for status in statuses:
                user_data[status.name_ar] = user_queryset.filter(status=status).count()
            shipment_by_user[user.get_full_name() or user.username] = user_data

        # توزيع عام حسب الحالة فقط
        shipment_by_status = {}
        for status in statuses:
            shipment_by_status[status.name_ar] = queryset.filter(status=status).count()

        # معلومات النطاق الزمني
        date_range = queryset.aggregate(
            first_date=Min('loading_date'),
            last_date=Max('loading_date'),
            total_shipments=Count('id'),
        )
        from_date = date_range['first_date'].strftime('%Y-%m-%d') if date_range['first_date'] else None
        to_date = date_range['last_date'].strftime('%Y-%m-%d') if date_range['last_date'] else None

        return Response({
            'all_shipments': all_shipments,
            'shipment_by_branch': shipment_by_branch,
            'shipment_by_city': shipment_by_city,
            'shipment_by_user': shipment_by_user,
            'shipment_by_status': shipment_by_status,
            'from_date': from_date,
            'to_date': to_date,
            'total_shipments_in_range': date_range['total_shipments'],
            'applied_filters': {
                'loading_date_gte': request.query_params.get('loading_date__gte'),
                'loading_date_lte': request.query_params.get('loading_date__lte')
            }
        })
