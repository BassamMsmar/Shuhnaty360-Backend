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

        # === التوزيع حسب الفروع وحالاتها
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

        # === التوزيع حسب المدن وحالاتها
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

        # === التوزيع حسب المستخدمين وحالاتهم
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

        # === التوزيع العام حسب الحالات
        shipment_by_status = dict(
            queryset
            .values(status_name=F('status__name_ar'))
            .annotate(total=Count('id'))
            .values_list('status_name', 'total')
        )

        # === معلومات المدى الزمني
        date_range = queryset.aggregate(
            first_date=Min('loading_date'),
            last_date=Max('loading_date'),
            total_shipments=Count('id'),
        )
        from_date = date_range['first_date'].strftime('%Y-%m-%d') if date_range['first_date'] else None
        to_date = date_range['last_date'].strftime('%Y-%m-%d') if date_range['last_date'] else None

        # === 📆 الشحنات لكل يوم خلال آخر 7 أيام (مع الأيام الفارغة)
        today = now().date()
        seven_days_ago = today - timedelta(days=6)

        daily_qs = (
            queryset
            .filter(loading_date__gte=seven_days_ago)
            .annotate(day=TruncDay('loading_date'))
            .values('day')
            .annotate(total=Count('id'))
        )
        daily_dict = {item['day'].strftime('%Y-%m-%d'): item['total'] for item in daily_qs}

        daily_stats = []
        for i in range(7):
            day = seven_days_ago + timedelta(days=i)
            day_str = day.strftime('%Y-%m-%d')
            daily_stats.append({
                'day': day_str,
                'total': daily_dict.get(day_str, 0)
            })

        # === 📅 الشحنات لكل أسبوع في آخر 4 أسابيع (مع الأسابيع الفارغة)
        weekly_qs = (
            queryset
            .filter(loading_date__gte=today - timedelta(weeks=4))
            .annotate(week=TruncWeek('loading_date'))
            .values('week')
            .annotate(total=Count('id'))
        )
        weekly_dict = {item['week'].strftime('%Y-%m-%d'): item['total'] for item in weekly_qs}

        weekly_stats = []
        start_of_this_week = today - timedelta(days=today.weekday())
        for i in range(4):
            week_start = (start_of_this_week - timedelta(weeks=3 - i))
            week_str = week_start.strftime('%Y-%m-%d')
            weekly_stats.append({
                'week': week_str,
                'total': weekly_dict.get(week_str, 0)
            })

        # === 🗓 الشحنات لكل شهر خلال آخر 12 شهرًا (مع الشهور الفارغة)
        monthly_qs = (
            queryset
            .filter(loading_date__gte=today.replace(day=1) - timedelta(days=365))
            .annotate(month=TruncMonth('loading_date'))
            .values('month')
            .annotate(total=Count('id'))
        )
        monthly_dict = {item['month'].strftime('%Y-%m'): item['total'] for item in monthly_qs}

        monthly_stats = []
        current_month = today.replace(day=1)
        for i in range(12):
            month = (current_month - timedelta(days=i * 30)).replace(day=1)
            month_str = month.strftime('%Y-%m')
            monthly_stats.insert(0, {
                'month': month_str,
                'total': monthly_dict.get(month_str, 0)
            })

        return Response({
            'all_shipments': all_shipments,
            'shipment_by_branch': shipment_by_branch,
            'shipment_by_city': shipment_by_city,
            'shipment_by_user': shipment_by_user,
            'shipment_by_status': shipment_by_status,
            'from_date': from_date,
            'to_date': to_date,
            'total_shipments_in_range': date_range['total_shipments'],

            # 🟩 إحصائيات زمنية
            'daily_stats_last_7_days': daily_stats,
            'weekly_stats_last_4_weeks': weekly_stats,
            'monthly_stats_last_12_months': monthly_stats,

            'applied_filters': {
                'loading_date_gte': request.query_params.get('loading_date__gte'),
                'loading_date_lte': request.query_params.get('loading_date__lte')
            }
        })
