import os
import django
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# إعداد متغير البيئة لمشروع Django الخاص بك
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')  # استبدل 'project' باسم مشروعك الفعلي
django.setup()

from cities.models import City
from shipments.models import ShipmentStatus
from drivers.models import TruckType


statuses = [
    {'name_ar': 'قيد الشحن', 'name_en': 'In Shipping'},
    {'name_ar': 'تم التوصيل', 'name_en': 'Delivered'},
    {'name_ar': 'مكتملة', 'name_en': 'Completed'},
    {'name_ar': 'متأخرة', 'name_en': 'Delayed'},
    {'name_ar': 'مرتجعة', 'name_en': 'Returned'},
    {'name_ar': 'ملغيه', 'name_en': 'Cancelled'},
]

cities = [
    {'en_city': 'Mecca', 'ar_city': 'مكة'},
    {'en_city': 'Riyadh', 'ar_city': 'الرياض'},
    {'en_city': 'Dammam', 'ar_city': 'الدمام'},
    {'en_city': 'Jeddah', 'ar_city': 'جدة'},
    {'en_city': 'Rabigh', 'ar_city': 'رابغ'},
    {'en_city': 'Abha', 'ar_city': 'ابها'},
    {'en_city': 'Abu Arish', 'ar_city': 'ابو عريش'},
    {'en_city': 'Ahad Al Masarihah', 'ar_city': 'احد المسارحة'},
    {'en_city': 'Ahad Rafidah', 'ar_city': 'احد رفيدة'},
    {'en_city': 'Al Bahah', 'ar_city': 'الباحة'},
    {'en_city': 'Jubail', 'ar_city': 'الجبيل'},
    {'en_city': 'Khobar', 'ar_city': 'الخبر'},
    {'en_city': 'Al Kharj', 'ar_city': 'الخرج'},
    {'en_city': 'Al Khurmah', 'ar_city': 'الخرمة'},
    {'en_city': 'Al Duwadimi', 'ar_city': 'الدوادمي / داودمي'},
    {'en_city': 'Taif', 'ar_city': 'الطائف'},
    {'en_city': 'Al Ardhiyah', 'ar_city': 'العرضية'},
    {'en_city': 'Al Qunfudhah', 'ar_city': 'القنفذه'},
    {'en_city': 'Al Majardah', 'ar_city': 'المجاردة'},
    {'en_city': 'Al Majma\'ah', 'ar_city': 'المجمعة'},
    {'en_city': 'Medina', 'ar_city': 'المدينة'},
    {'en_city': 'Al Muzaylif', 'ar_city': 'المظيلف'},
    {'en_city': 'Al Mandaq', 'ar_city': 'المندق'},
    {'en_city': 'Al Hofuf', 'ar_city': 'الهفوف'},
    {'en_city': 'Buraidah', 'ar_city': 'بريدة'},
    {'en_city': 'Baish', 'ar_city': 'بيش'},
    {'en_city': 'Bisha', 'ar_city': 'بيشة'},
    {'en_city': 'Tabuk', 'ar_city': 'تبوك'},
    {'en_city': 'Jizan', 'ar_city': 'جيزان'},
    {'en_city': 'Hail', 'ar_city': 'حايل'},
    {'en_city': 'Hafar Al-Batin', 'ar_city': 'حفر الباطن'},
    {'en_city': 'Khamis Mushait', 'ar_city': 'خميس مشيط'},
    {'en_city': 'Riyadh Al Khabra', 'ar_city': 'رياض الخبر'},
    {'en_city': 'Sakaka', 'ar_city': 'سكاكا'},
    {'en_city': 'Sharurah', 'ar_city': 'شرورة'},
    {'en_city': 'Sabya', 'ar_city': 'صبيا'},
    {'en_city': 'Tabrjal', 'ar_city': 'طبرجل'},
    {'en_city': 'Arar', 'ar_city': 'عرعر'},
    {'en_city': 'Najran', 'ar_city': 'نجران'},
    {'en_city': 'Yanbu', 'ar_city': 'ينبع'},
    {'en_city': 'Unayzah', 'ar_city': 'عنيزة'},
    {'en_city': 'Al Darb', 'ar_city': 'الدرب'},
    {'en_city': 'Turbah', 'ar_city': 'تربة'},
    {'en_city': 'Al Aqiq', 'ar_city': 'العقيق'},
    {'en_city': 'Qilwah', 'ar_city': 'قلوه'},
    {'en_city': 'Al Maqaiid', 'ar_city': 'المقاعد'},
    {'en_city': 'Mahayel', 'ar_city': 'محايل'},
    {'en_city': 'As Sulayyil', 'ar_city': 'السليل'},
    {'en_city': 'Al Kamil', 'ar_city': 'الكامل'},
    {'en_city': 'Namirah', 'ar_city': 'نمره'}
]

truck_types = [
    {'name_ar': 'سطحه جاف 24طن', 'name_en': 'Flatbed Dry 24 Ton', 'description': 'سطحه جاف لحمل الأحمال حتى 24 طن'},
    {'name_ar': 'ستاره 24طن', 'name_en': 'Curtain Side 24 Ton', 'description': 'ستاره بحمولة تصل إلى 24 طن'},
    {'name_ar': 'براد 24طن', 'name_en': 'Refrigerated Truck 24 Ton', 'description': 'شاحنة مبردة لحمل البضائع حتى 24 طن'},
    {'name_ar': 'جوانب عالي 15متر', 'name_en': 'High Sides 15 Meter', 'description': 'شاحنة بجوانب عالية بطول 15 متر'},

    {'name_ar': 'لوري جاف 10طن', 'name_en': 'Dry Lorry 10 Ton', 'description': 'لوري جاف بوزن 10 طن'},
    {'name_ar': 'لوري مبرد 10طن', 'name_en': 'Refrigerated Lorry 10 Ton', 'description': 'لوري مبرد بوزن 10 طن'},
    {'name_ar': 'لوري تثليج 10 طن', 'name_en': 'Freezing Lorry 10 Ton', 'description': 'لوري تثليج بوزن 10 طن'},

    {'name_ar': 'دينه جاف 5 طن', 'name_en': 'Dry Dyna 5 Ton', 'description': 'دينه جاف بوزن 5 طن'},
    {'name_ar': 'دينه مبرد 5 طن', 'name_en': 'Refrigerated Dyna 5 Ton', 'description': 'دينه مبرد بوزن 5 طن'},
    {'name_ar': 'دينة تثليج 5 طن', 'name_en': 'Freezing Dyna 5 Ton', 'description': 'دينة تثليج بوزن 5 طن'},
]


for data in cities:
    obj, created = City.objects.get_or_create(
        ar_city=data['ar_city'],  # الاعتماد على الاسم العربي لأنه unique
        defaults={'en_city': data['en_city']}
    )
    if created:
        print(f'✅ City {data["en_city"]} created')
    else:
        print(f'ℹ️ City {data["en_city"]} already exists')

for data in truck_types:
    obj, created = TruckType.objects.get_or_create(
        name_ar=data['name_ar'],  # الاعتماد على الاسم العربي
        defaults={
            'name_en': data['name_en'],
            'description': data['description']
        }
    )
    if created:
        print(f'✅ Truck Type {data["name_en"]} created')
    else:
        print(f'ℹ️ Truck Type {data["name_en"]} already exists')

for data in statuses:
    obj, created = ShipmentStatus.objects.get_or_create(
        name_ar=data['name_ar'],  # الاعتماد على الاسم العربي
        defaults={'name_en': data['name_en']}
    )
    if created:
        print(f'✅ Shipment Status {data["name_en"]} created')
    else:
        print(f'ℹ️ Shipment Status {data["name_en"]} already exists')
