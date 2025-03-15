import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from shipments.models import Shipment, ShipmentStatus
from recipient.models import Recipient
from drivers.models import Driver
from clients.models import Client, Branch
from cities.models import City
from django.contrib.auth.models import User
import random
from faker import Faker

# إعداد متغير البيئة لمشروع Django الخاص بك
# استبدل 'project' باسم مشروعك الفعلي


fake = Faker('ar_SA')


CITIES = [('Jeddah', 'جدة'), ('Riyadh', 'الرياض'), ('Dammam', 'الدمام'), ('Makkah', 'مكة'), ('Madinah',
                                                                                             'المدينة'), ('Abha', 'أبها'), ('Jizan', 'جيزان'), ('Tabuk', 'تبوك'), ('Hail', 'حائل'), ('Qassim', 'القصيم')]
users = ['صالح حسين', 'حسين اليافعي', 'بندر الهمداني ',
         'نشوان طفيان', 'خالد عثمان', 'احمد سالم']

clints = ['ارنون', 'ابوداوود ', ' المعتمدون', 'المنتجات الحديثة', 'العثيم']

# Create a superuser


def create_superuser():
    User.objects.create_superuser(
        'admin', 'admin@admin.com', 'admin', first_name='Admin', last_name='Admin')

# Create 5 Users


def create_user():
    for i, user in enumerate(users, start=1):
        User.objects.create_user(
            Faker().user_name(), Faker().email(), 'password', first_name=user)
        print(f'User {i} created')


# Create 5 Cities
def create_city():
    for i, (ar_city, en_city) in enumerate(CITIES, start=1):
        City.objects.create(ar_city=ar_city, en_city=en_city)
        print(f'City {i} created')


# Create 5 Clients
def create_client():

    for i, clint in enumerate(clints, start=1):
        Client.objects.create(name=clint, address=Faker().address(
        ), phone_number=fake.numerify(text='############'), email=Faker().email())
        print(f'Client {i} created')

# Create 10 Branches


def create_branch():
    clients = Client.objects.all()
    cities = City.objects.all()
    for i in range(1, 11):
        Branch.objects.create(client=random.choice(clients), name=Faker().company(), city=random.choice(
            cities), address=Faker().address(), phone_number=fake.numerify(text='############'))
        print(f'Branch {i} created')


def create_shipment_status():
    ShipmentStatus.objects.create(name_en='In Shipping', name_ar='قيد الشحن')
    ShipmentStatus.objects.create(name_en='In Transit', name_ar='في الطريق')
    ShipmentStatus.objects.create(name_en='Delivered', name_ar='تم التوصيل')
    ShipmentStatus.objects.create(name_en='Returned', name_ar='تم الإرجاع')
    ShipmentStatus.objects.create(
        name_en='Under Review', name_ar='قيد المراجعة')
    ShipmentStatus.objects.create(name_en='Cancelled', name_ar='تم الإلغاء')
    print('Shipment statuses created')


# Create 10 Drivers
def create_driver():
    for i in range(1, 11):
        Driver.objects.create(
            name=fake.first_name_male(),
            phone_number=fake.numerify(text='############'),
            nationality=fake.country(),
            language=random.choice(['en', 'ar', 'ur']),
            identity_number=fake.numerify(text='############'),
            vehicle_number=fake.numerify(text='########'),
            status=random.choice(['available', 'busy', 'offline'])
        )
        print(f'Driver {i} created')


# Create 10 Recipients
def create_recipient():
    cities = City.objects.all()
    for i in range(1, 11):
        Recipient.objects.create(
            name=Faker().name(),
            phone_number=fake.numerify(text='############'),
            address=Faker().address(),
            city=random.choice(cities))
        print(f'Recipient {i} created')


def create_shipment():
    user = User.objects.all()
    driver = Driver.objects.all()
    customer_branch = Branch.objects.all()
    recipient = Recipient.objects.all()
    status = ShipmentStatus.objects.all()
    cities = City.objects.all()
    for i in range(1, 100):
        Shipment.objects.create(
            user=random.choice(user),
            driver=random.choice(driver),
            customer_branch=random.choice(customer_branch),
            customer_invoice_number=Faker().numerify(text='##########'),
            recipient=random.choice(recipient),
            origin_city=random.choice(cities),
            destination_city=random.choice(cities),
            fare=Faker().numerify(text='###'),
            premium=Faker().numerify(text='###'),
            fare_return=Faker().numerify(text='###'),
            days_stayed=Faker().numerify(text='#'),
            stay_cost=Faker().numerify(text='###'),
            deducted=Faker().numerify(text='###'),
            status=random.choice(status),
            days_to_arrive=random.choice([1, 2, 3, 4, 5]),
            notes=Faker().sentence(),
        )

        print(f'shipment {i} created')


#create_superuser()
#create_user()
#create_city()
create_client()
create_branch()
create_driver()
create_recipient()
create_shipment_status()
create_shipment()
