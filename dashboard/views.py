from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from django.db.models import Count, Min, Max, F
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth
from django.utils.timezone import now
from datetime import timedelta
from django_filters.rest_framework import DjangoFilterBackend

from shipments.models import Shipment, ShipmentStatus
from profile_company.models import CompanyBranch
from cities.models import City
from django.contrib.auth import get_user_model

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

        # توزيع الشحنات حسب الفروع وحالاتها
        branch_status = queryset.values(
            branch_name=F('user__company_branch__branch_name_ar'),
            status_name=F('status__name_ar')
        ).annotate(total=Count('id'))

        shipment_by_branch = {}
        for item in branch_status:
            branch = item['branch_name']
            status = item['status_name']
            shipment_by_branch.setdefault(branch, {"كل الشحنات": 0})
            shipment_by_branch[branch][status] = item['total']
            shipment_by_branch[branch]["كل الشحنات"] += item['total']

        # توزيع الشحنات حسب المدن وحالاتها
        city_status = queryset.values(
            city_name=F('destination_city__ar_city'),
            status_name=F('status__name_ar')
        ).annotate(total=Count('id'))

        shipment_by_city = {}
        for item in city_status:
            city = item['city_name']
            status = item['status_name']
            shipment_by_city.setdefault(city, {"كل الشحنات": 0})
            shipment_by_city[city][status] = item['total']
            shipment_by_city[city]["كل الشحنات"] += item['total']

        # توزيع الشحنات حسب المستخدمين وحالاتهم
        user_status = queryset.values(
            user_name=F('user__username'),
            status_name=F('status__name_ar')
        ).annotate(total=Count('id'))

        shipment_by_user = {}
        for item in user_status:
            user = item['user_name']
            status = item['status_name']
            shipment_by_user.setdefault(user, {"كل الشحنات": 0})
            shipment_by_user[user][status] = item['total']
            shipment_by_user[user]["كل الشحنات"] += item['total']

        # توزيع عام حسب الحالة فقط
        shipment_by_status = dict(
            queryset
            .values(status_name=F('status__name_ar'))
            .annotate(total=Count('id'))
            .values_list('status_name', 'total')
        )

        # معلومات النطاق الزمني
        date_range = queryset.aggregate(
            first_date=Min('loading_date'),
            last_date=Max('loading_date'),
            total_shipments=Count('id'),
        )
        from_date = date_range['first_date'].strftime('%Y-%m-%d') if date_range['first_date'] else None
        to_date = date_range['last_date'].strftime('%Y-%m-%d') if date_range['last_date'] else None

        # === 📆 عدد الشحنات حسب الأيام (آخر 7 أيام)
        last_7_days = queryset.filter(loading_date__gte=now().date() - timedelta(days=6))
        daily_stats = (
            last_7_days
            .annotate(day=TruncDay('loading_date'))
            .values('day')
            .annotate(total=Count('id'))
            .order_by('day')
        )

        # === 📆 عدد الشحنات حسب الأسابيع (آخر 4 أسابيع)
        last_4_weeks = queryset.filter(loading_date__gte=now().date() - timedelta(weeks=4))
        weekly_stats = (
            last_4_weeks
            .annotate(week=TruncWeek('loading_date'))
            .values('week')
            .annotate(total=Count('id'))
            .order_by('week')
        )

        # === 📆 عدد الشحنات حسب الأشهر (آخر 12 شهر)
        last_12_months = queryset.filter(loading_date__gte=now().date().replace(day=1) - timedelta(days=365))
        monthly_stats = (
            last_12_months
            .annotate(month=TruncMonth('loading_date'))
            .values('month')
            .annotate(total=Count('id'))
            .order_by('month')
        )

        return Response({
            'all_shipments': all_shipments,
            'shipment_by_branch': shipment_by_branch,
            'shipment_by_city': shipment_by_city,
            'shipment_by_user': shipment_by_user,
            'shipment_by_status': shipment_by_status,
            'from_date': from_date,
            'to_date': to_date,
            'total_shipments_in_range': date_range['total_shipments'],

            # 📊 الإحصائيات الزمنية
            'daily_stats_last_7_days': daily_stats,
            'weekly_stats_last_4_weeks': weekly_stats,
            'monthly_stats_last_12_months': monthly_stats,

            'applied_filters': {
                'loading_date_gte': request.query_params.get('loading_date__gte'),
                'loading_date_lte': request.query_params.get('loading_date__lte')
            }
        })
