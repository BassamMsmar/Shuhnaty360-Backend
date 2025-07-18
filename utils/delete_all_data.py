import os
import django
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# إعداد متغير البيئة لمشروع Django الخاص بك
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')  # استبدل 'project' باسم مشروعك الفعلي
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
from clients.models import Client, Branch
from drivers.models import Driver, TruckType
from recipient.models import Recipient
from shipments.models import Shipment, ShipmentHistory, ShipmentStatus
from profile_company.models import CompanyProfile, CompanyBranch
from cities.models import City

input("Do you want to delete all data? (y/n)")
print("Deleting all data...")

if input("Do you want to delete all data? (y/n)") == 'y':
    User.objects.all().delete()
    Shipment.objects.all().delete()
    ShipmentHistory.objects.all().delete()
    ShipmentStatus.objects.all().delete()
    Recipient.objects.all().delete()
    Driver.objects.all().delete()
    TruckType.objects.all().delete()
    Branch.objects.all().delete()
    Client.objects.all().delete()
    City.objects.all().delete()
    User.objects.filter(is_superuser=False).delete()
    print("All data deleted successfully.")
else:
    print("No data deleted.")

