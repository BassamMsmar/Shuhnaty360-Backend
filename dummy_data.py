import os
import django

# إعداد متغير البيئة لمشروع Django الخاص بك
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')  # استبدل 'project' باسم مشروعك الفعلي
django.setup()

from faker import Faker
import random

from django.contrib.auth.models import User
from cities.models import City
from clients.models import Client, Branch
from drivers.models import Driver
from recipient.models import Recipient
import faker

CITIES = [('Jeddah', 'جدة'), ('Riyadh', 'الرياض'), ('Dammam', 'الدمام'), ('Makkah', 'مكة'), ('Madinah', 'المدينة')]

# Create a superuser
def create_superuser():
    User.objects.create_superuser('admin', 'admin@admin.com', 'admin', first_name='Admin', last_name='Admin')

# Create 5 Users
def create_user():
    for i in range(1, 6):
        User.objects.create_user(Faker().user_name(), Faker().email(), 'password', first_name=Faker().first_name(),last_name=Faker().last_name())
        print(f'User {i} created')

# Create 5 Cities
def create_city():
    for i, (ar_city, en_city) in enumerate(CITIES, start=1):
        City.objects.create(ar_city=ar_city, en_city=en_city)
        print(f'City {i} created')


# Create 5 Clients
def create_client():
    for i in range(1, 6):
        Client.objects.create(name=Faker().company(), address=Faker().address(), phone_number=Faker().phone_number(), email=Faker().email())
        print(f'Client {i} created')

# Create 10 Branches
def create_branch():
    clients = Client.objects.all()
    cities = City.objects.all()
    for i in range(1, 11):
        Branch.objects.create(client=random.choice(clients), name=Faker().company(), city=random.choice(cities), address=Faker().address(), phone_number=Faker().phone_number())
        print(f'Branch {i} created')


# Create 10 Drivers
def create_driver():
    for i in range(1, 11):
        Driver.objects.create(
            name=Faker().name(),
            phone_number=Faker().phone_number(),
            nationality=Faker().country(),
            language = random.choice(['en', 'ar', 'ur']),
            identity_number=Faker().numerify(text='############'),
            vehicle_number=Faker().numerify(text='########'),
            status=random.choice(['available', 'busy', 'offline']))
        print(f'Driver {i} created')

# Create 10 Recipients
def create_recipient():
    cities = City.objects.all()
    for i in range(1, 11):
        Recipient.objects.create(
            name=Faker().name(),
            phone_number=Faker().phone_number(),
            address=Faker().address(),
            city=random.choice(cities))
        print(f'Recipient {i} created')



create_superuser()
create_user()
create_city()
create_client()
create_branch()
create_driver()
create_recipient()
