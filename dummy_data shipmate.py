import os
import django

# إعداد متغير البيئة لمشروع Django الخاص بك
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')  # استبدل 'project' باسم مشروعك الفعلي
django.setup()

from faker import Faker
import random
import uuid
from datetime import timedelta
from django.utils import timezone

from django.contrib.auth import get_user_model

User = get_user_model()
from cities.models import City
from clients.models import Client, Branch
from drivers.models import Driver, TruckType
from recipient.models import Recipient
from shipments.models import Shipment, ShipmentStatus, ShipmentHistory
from profile_company.models import CompanyProfile, CompanyBranch

CITIES = [('جدة', 'Jeddah'), ('الرياض', 'Riyadh'), ('الدمام', 'Dammam'), ('مكة', 'Makkah'), ('المدينة', 'Madinah')]

# Create a superuser
def create_superuser():
    # Check if superuser already exists
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin', 
            email='admin@admin.com', 
            password='admin', 
            first_name='Admin', 
            last_name='Admin',
            phone='1234567890'
        )
        print('Superuser created')
    else:
        print('Superuser already exists')

# Create 5 Users
def create_user():
    fake = Faker()
    branches = list(CompanyBranch.objects.all())
    
    for i in range(1, 6):
        username = fake.user_name()
        # Make sure username is unique
        while User.objects.filter(username=username).exists():
            username = fake.user_name()
        
        # Randomly assign a company branch to some users
        company_branch = random.choice(branches) if branches and random.choice([True, False]) else None
            
        User.objects.create_user(
            username=username, 
            email=fake.email(), 
            password='password', 
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            phone=fake.phone_number()[:10],
            company_branch=company_branch
        )
        print(f'User {i} created')

# Create 5 Cities
def create_city():
    for i, (ar_city, en_city) in enumerate(CITIES, start=1):
        # Check if city already exists by either Arabic or English name
        if not City.objects.filter(en_city=en_city).exists() and not City.objects.filter(ar_city=ar_city).exists():
            City.objects.create(ar_city=ar_city, en_city=en_city)
            print(f'City {en_city} ({ar_city}) created')
        else:
            print(f'City {en_city} ({ar_city}) already exists')

# Create company profiles
def create_company_profiles():
    fake = Faker()
    cities = list(City.objects.all())
    
    # Check if company profiles already exist
    if CompanyProfile.objects.count() >= 3:
        print('Company profiles already exist')
        return
        
    for i in range(1, 4):  # Create 3 company profiles
        company_name_en = f'{fake.company()} Company {i}'
        company_name_ar = f'شركة {fake.company()} {i}'
        
        # Check if a company with this name already exists
        if not CompanyProfile.objects.filter(company_name_en=company_name_en).exists():
            CompanyProfile.objects.create(
                company_name_ar=company_name_ar,
                company_name_en=company_name_en,
                company_description_ar=fake.paragraph(),
                company_description_en=fake.paragraph(),
                main_phone_number=fake.phone_number()[:10],
                secondary_phone_number=fake.phone_number()[:10] if random.choice([True, False]) else None,
                email=fake.company_email(),
                website=f'https://www.{fake.domain_name()}' if random.choice([True, False]) else None,
                address=fake.address(),
                city=random.choice(cities) if cities else None,
                is_active=True,
                created_at=timezone.now() - timedelta(days=random.randint(30, 365)),
                updated_at=timezone.now() - timedelta(days=random.randint(1, 30))
            )
            print(f'Company Profile {i} created')
        else:
            print(f'Company profile {company_name_en} already exists')

# Create company branches
def create_company_branches():
    fake = Faker()
    companies = CompanyProfile.objects.all()
    cities = City.objects.all()
    
    for company in companies:
        # Create 2-4 branches for each company
        for i in range(1, random.randint(2, 5)):
            CompanyBranch.objects.create(
                company=company,
                branch_name_ar=f'فرع {fake.city()} {i}',
                branch_name_en=f'{fake.city()} Branch {i}',
                main_phone_number=fake.phone_number()[:10],
                secondary_phone_number=fake.phone_number()[:10] if random.choice([True, False]) else None,
                email=fake.company_email(),
                address=fake.address(),
                city=random.choice(cities) if cities.exists() else None,
                is_active=True,
                created_at=timezone.now() - timedelta(days=random.randint(30, 365)),
                updated_at=timezone.now() - timedelta(days=random.randint(1, 30))
            )
            print(f'Company Branch created for {company}')


# Create 5 Clients
def create_client():
    fake = Faker()
    
    # Check if we already have enough clients
    if Client.objects.count() >= 5:
        print('Clients already exist')
        return
        
    for i in range(1, 6):
        client_email = fake.email()
        # Check if a client with this email already exists
        if not Client.objects.filter(email=client_email).exists():
            Client.objects.create(
                name=fake.company(), 
                address=fake.address(), 
                phone_number=fake.phone_number()[:10], 
                email=client_email,
                second_phone_number=fake.phone_number()[:10] if random.choice([True, False]) else None,
                Commercial_registration_number=fake.numerify(text='##########') if random.choice([True, False]) else None,
                dicription=fake.paragraph() if random.choice([True, False]) else None
            )
            print(f'Client {i} created')
        else:
            print(f'Client with email {client_email} already exists')

# Create 10 Branches
def create_branch():
    fake = Faker()
    clients = Client.objects.all()
    cities = City.objects.all()
    for i in range(1, 11):
        Branch.objects.create(
            client=random.choice(clients), 
            name=fake.company(), 
            city=random.choice(cities), 
            address=fake.address(), 
            phone_number=fake.phone_number()[:10],
            name_address=fake.street_name() if random.choice([True, False]) else None,
            second_phone_number=fake.phone_number()[:10] if random.choice([True, False]) else None
        )
        print(f'Branch {i} created')
# Create Truck Types
def create_truck_types():
    truck_types = [
        {'name_ar': 'شاحنة صغيرة', 'name_en': 'Small Truck', 'description': 'شاحنة صغيرة للشحنات الخفيفة'},
        {'name_ar': 'شاحنة متوسطة', 'name_en': 'Medium Truck', 'description': 'شاحنة متوسطة للشحنات المتوسطة'},
        {'name_ar': 'شاحنة كبيرة', 'name_en': 'Large Truck', 'description': 'شاحنة كبيرة للشحنات الثقيلة'},
        {'name_ar': 'شاحنة مبردة', 'name_en': 'Refrigerated Truck', 'description': 'شاحنة مبردة للمواد الغذائية'}
    ]
    
    for i, truck_type in enumerate(truck_types, 1):
        # Check if truck type already exists
        if not TruckType.objects.filter(name_en=truck_type['name_en']).exists():
            TruckType.objects.create(
                name_ar=truck_type['name_ar'],
                name_en=truck_type['name_en'],
                description=truck_type['description']
            )
            print(f'Truck Type {i} created')
        else:
            print(f'Truck Type {truck_type["name_en"]} already exists')

# Create Shipment Statuses
def create_shipment_status():
    statuses = [
        {'name_en': 'In Shipping', 'name_ar': 'قيد الشحن'},
        {'name_en': 'In Transit', 'name_ar': 'في الطريق'},
        {'name_en': 'Delivered', 'name_ar': 'تم التوصيل'},
        {'name_en': 'Returned', 'name_ar': 'تم الإرجاع'},
        {'name_en': 'Under Review', 'name_ar': 'قيد المراجعة'},
        {'name_en': 'Cancelled', 'name_ar': 'تم الإلغاء'}
    ]
    
    # Check if statuses already exist
    if ShipmentStatus.objects.count() >= len(statuses):
        print('Shipment statuses already exist')
        return
    
    for status in statuses:
        # Check if status already exists
        if not ShipmentStatus.objects.filter(name_en=status['name_en']).exists():
            ShipmentStatus.objects.create(name_en=status['name_en'], name_ar=status['name_ar'])
            print(f'Shipment status {status["name_en"]} created')
        else:
            print(f'Shipment status {status["name_en"]} already exists')
    
    print('Shipment statuses creation completed')


# Create 10 Drivers
def create_driver():
    fake = Faker()
    truck_types = list(TruckType.objects.all())
    
    for i in range(1, 11):
        Driver.objects.create(
            name=fake.name(),
            phone_number=fake.phone_number()[:10],
            nationality=fake.country(),
            language=random.choice(['en', 'ar', 'ur']),
            identity_number=fake.numerify(text='############'),
            vehicle_number=fake.numerify(text='########'),
            truck_type=random.choice(truck_types) if truck_types else None,
            status=random.choice(['available', 'busy', 'offline']),
            is_active=random.choice([True, True, True, False]),  # 75% chance of being active
            created_at=timezone.now() - timedelta(days=random.randint(1, 365)),
            updated_at=timezone.now() - timedelta(days=random.randint(0, 30))
        )
        print(f'Driver {i} created')

# Create 10 Recipients
def create_recipient():
    fake = Faker()
    cities = City.objects.all()
    for i in range(1, 11):
        Recipient.objects.create(
            name=fake.name(),
            phone_number=fake.phone_number()[:10],
            address=fake.address(),
            city=random.choice(cities),
            second_phone_number=fake.phone_number()[:10] if random.choice([True, False]) else None,
            email=fake.email() if random.choice([True, False]) else None
        )
        print(f'Recipient {i} created')

def create_shipment():
    # Check if we already have shipments
    if Shipment.objects.count() > 1000:
        print('Shipments already exist')
        return
        
    fake = Faker()
    users = list(User.objects.all())
    drivers = list(Driver.objects.all())
    branches = list(Branch.objects.all())
    recipients = list(Recipient.objects.all())
    statuses = list(ShipmentStatus.objects.all())
    cities = list(City.objects.all())
    clients = list(Client.objects.all())
    
    # Make sure we have all the necessary data
    if not all([users, drivers, branches, recipients, statuses, cities, clients]):
        print('Missing required data for shipment creation')
        return
    
    # Create fewer shipments for testing
    for i in range(1, 20):
        # Create a shipment with proper client-branch relationship
        client = random.choice(clients)
        client_branches = Branch.objects.filter(client=client)
        branch = random.choice(client_branches) if client_branches.exists() else random.choice(branches)
        
        # Create base shipment
        loading_date = timezone.now() - timedelta(days=random.randint(1, 30))
        days_to_arrive = random.choice([1, 2, 3, 4, 5])
        expected_arrival = loading_date + timedelta(days=days_to_arrive)
        
        # Randomly decide if shipment has been delivered
        is_delivered = random.choice([True, False])
        actual_delivery = loading_date + timedelta(days=random.randint(1, days_to_arrive+2)) if is_delivered else None
        
        # Select appropriate status based on delivery state
        if is_delivered:
            status = next((s for s in statuses if s.name_en == 'Delivered'), random.choice(statuses))
        else:
            non_delivered_statuses = [s for s in statuses if s.name_en != 'Delivered']
            status = random.choice(non_delivered_statuses) if non_delivered_statuses else random.choice(statuses)
        
        shipment = Shipment.objects.create(
            user=random.choice(users),
            driver=random.choice(drivers),
            client=client,
            client_branch=branch,
            client_invoice_number=fake.numerify(text='##########'),
            notes_customer=fake.paragraph() if random.choice([True, False]) else None,
            recipient=random.choice(recipients),
            notes_recipient=fake.paragraph() if random.choice([True, False]) else None,
            origin_city=random.choice(cities),
            destination_city=random.choice(cities),
            fare=random.randint(100, 1000),
            premium=random.randint(50, 200) if random.choice([True, False]) else None,
            fare_return=random.randint(50, 200) if random.choice([True, False]) else None,
            days_stayed=random.randint(0, 5) if random.choice([True, False]) else None,
            stay_cost=random.randint(50, 200) if random.choice([True, False]) else None,
            deducted=random.randint(10, 100) if random.choice([True, False]) else None,
            status=status,
            loading_date=loading_date,
            days_to_arrive=days_to_arrive,
            expected_arrival_date=expected_arrival,
            actual_delivery_date=actual_delivery,
            weight=round(random.uniform(0.5, 10.0), 2) if random.choice([True, False]) else None,
            contents=fake.paragraph() if random.choice([True, False]) else None,
            notes=fake.sentence() if random.choice([True, False]) else None,
            created_at=loading_date - timedelta(days=random.randint(1, 3)),
            loading_at=loading_date,
            updated_at=timezone.now() - timedelta(days=random.randint(0, 5))
        )
        
        # Create shipment history entries
        create_shipment_history(shipment, statuses, users)
            
        print(f'Shipment {i} created')

# Create shipment history entries for a shipment
def create_shipment_history(shipment, statuses, users):
    fake = Faker()
    # Always create an initial status entry
    initial_status = next((s for s in statuses if s.name_en == 'In Shipping'), random.choice(statuses))
    
    ShipmentHistory.objects.create(
        shipment=shipment,
        status=initial_status,
        updated_at=shipment.created_at,
        user=random.choice(users),
        notes=fake.sentence() if random.choice([True, False]) else None
    )
    
    # Add 1-3 random status updates
    for _ in range(random.randint(1, 3)):
        update_time = shipment.created_at + timedelta(days=random.randint(1, 5))
        if update_time > timezone.now():
            update_time = timezone.now()
            
        ShipmentHistory.objects.create(
            shipment=shipment,
            status=random.choice(statuses),
            updated_at=update_time,
            user=random.choice(users),
            notes=fake.sentence() if random.choice([True, False]) else None
        )
    
    # If shipment is delivered, add a delivered status
    if shipment.actual_delivery_date:
        delivered_status = next((s for s in statuses if s.name_en == 'Delivered'), None)
        if delivered_status:
            ShipmentHistory.objects.create(
                shipment=shipment,
                status=delivered_status,
                updated_at=shipment.actual_delivery_date,
                user=random.choice(users),
                notes=fake.sentence() if random.choice([True, False]) else None
            )



# Clear existing data (uncomment if you want to clear data before creating new)
'''
ShipmentHistory.objects.all().delete()
Shipment.objects.all().delete()
ShipmentStatus.objects.all().delete()
Recipient.objects.all().delete()
Driver.objects.all().delete()
TruckType.objects.all().delete()
Branch.objects.all().delete()
Client.objects.all().delete()
City.objects.all().delete()
User.objects.filter(is_superuser=False).delete()
'''

# Create data in the correct order
print('Starting data creation...')
# create_city()
# create_company_profiles()
# create_company_branches()
# create_superuser()
# create_user()
# create_client()
# create_branch()
# create_truck_types()
# create_driver()
# create_recipient()
# create_shipment_status()
create_shipment()
print('Data creation completed successfully!')
