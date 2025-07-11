import os
import django
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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
from clients.models import Client, Branch
from drivers.models import Driver, TruckType
from recipient.models import Recipient
from shipments.models import Shipment, ShipmentHistory, ShipmentStatus
from profile_company.models import CompanyProfile, CompanyBranch
from cities.models import City


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


# Create company profiles
def create_company_profiles():
    fake = Faker()
    cities = list(City.objects.all())
    
    # Check if company profile already exists
    if CompanyProfile.objects.exists():
        print('Company profile already exists')
        return None
    
    # Generate phone numbers with max 20 characters
    def get_phone_number():
        # Generate phone number and ensure it's not longer than 20 characters
        phone = fake.numerify(text='+9665########')
        return phone[:10]
    
    # Create one company profile
    company_name_en = 'Aljeed Transportations'
    company_name_ar = 'شركة الجيد للنقليات'
    
    company = CompanyProfile.objects.create(
        company_name_ar=company_name_ar,
        company_name_en=company_name_en,
        company_description_ar='شركة رائدة في مجال الشحن والتوصيل',
        company_description_en='Leading company in shipping and delivery services',
        main_phone_number=get_phone_number(),
        secondary_phone_number=get_phone_number(),
        email='info@aljeed.com',
        website='https://www.aljeed.com',
        address='الرياض، المملكة العربية السعودية',
        city=random.choice(cities) if cities else None,
        is_active=True,
        created_at=timezone.now() - timedelta(days=365),
        updated_at=timezone.now() - timedelta(days=30)
    )
    print('Company Profile created successfully')
    return company

# Create company branches
def create_company_branches():
    fake = Faker()
    cities = list(City.objects.all())
    
    # Get the company or create it if it doesn't exist
    company = CompanyProfile.objects.first()
    if not company:
        company = create_company_profiles()
        if not company:  # If creation failed
            return
    
    # Check if branches already exist
    if CompanyBranch.objects.count() >= 6:
        print('Branches already exist')
        return
    
    branch_cities = random.sample(cities, min(6, len(cities)))  # Get 6 unique cities or less if not enough
    
    # Create exactly 6 branches
    for i in range(1, 7):
        city = branch_cities[i % len(branch_cities)] if branch_cities else None
        branch_name = f'الفرع الرئيسي {i}' if i == 1 else f'فرع {fake.city()[:15]}'
        
        CompanyBranch.objects.create(
            company=company,
            branch_name_ar=branch_name,
            branch_name_en=f'{fake.city()} Branch {i}',
            main_phone_number=fake.phone_number()[:10],
            secondary_phone_number=fake.phone_number()[:10] if random.choice([True, False]) else None,
            email=fake.company_email(),
            address=fake.address(),
            city=city,
            is_active=True,
            created_at=timezone.now() - timedelta(days=random.randint(30, 365)),
            updated_at=timezone.now() - timedelta(days=random.randint(1, 30))
        )
        print(f'Company Branch created for {company}')

# Create 100 Users
def create_user(users):
    fake = Faker()
    branches = list(CompanyBranch.objects.all())
    
    for i in range(1, users):
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

    print(f'Users created successfully!')

# Create 200 Clients
def create_client(clients):
    fake = Faker()
    
    # Check if we already have enough clients
    if Client.objects.count() >= clients:
        print('Clients already exist')
        return
        
    for i in range(1, clients):
        client_email = fake.email()
        # Generate phone number with max 20 characters
        phone = fake.phone_number()[:10]
        second_phone = fake.phone_number()[:10] if random.choice([True, False]) else None
        
        # Check if a client with this email already exists
        if not Client.objects.filter(email=client_email).exists():
            Client.objects.create(
                name=fake.company(), 
                address=fake.address(), 
                phone_number=phone, 
                email=client_email,
                second_phone_number=second_phone,
                Commercial_registration_number=fake.numerify(text='##########') if random.choice([True, False]) else None,
                dicription=fake.paragraph() if random.choice([True, False]) else None
            )
            print(f'Client {i} created')
        else:
            print(f'Client with email {client_email} already exists')

# Create 100 Branches
def create_branch(clients):
    fake = Faker()
    clients = Client.objects.all()
    cities = City.objects.all()
    for i in range(1, clients):
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

# Create 1000 Drivers
def create_driver(drivers):
    fake = Faker()
    truck_types = list(TruckType.objects.all())

    if truck_types:
        for i in range(1, drivers):
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

# Create 500 Recipients
def create_recipient(recipients):
    fake = Faker()
    cities = City.objects.all()
    
    if cities.exists():
        created_count = 0
        attempts = 0
        
        while created_count < recipients and attempts < 1000:  # محاولة محددة العدد لتفادي حلقة لا نهائية
            email = fake.email() if random.choice([True, False]) else None
            
            # تأكد من عدم تكرار البريد
            if email and Recipient.objects.filter(email=email).exists():
                attempts += 1
                continue

            try:
                Recipient.objects.create(
                    name=fake.name(),
                    phone_number=fake.phone_number()[:10],
                    address=fake.address(),
                    city=random.choice(cities),
                    second_phone_number=fake.phone_number()[:10] if random.choice([True, False]) else None,
                    email=email
                )
                created_count += 1
                print(f'✅ Recipient {created_count} created')
            except Exception as e:
                print(f'❌ Error creating recipient {created_count + 1}: {e}')
                attempts += 1
    else:
        print("⚠️ No cities found.")

# Create 10,000 Shipments
def create_shipment(shipments):
    # Check if we already have shipments
    if Shipment.objects.count() > shipments:
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
        if not users:
            print('No users found')
        if not drivers:
            print('No drivers found')
        if not branches:
            print('No branches found')
        if not recipients:
            print('No recipients found')
        if not statuses:
            print('No statuses found')
        if not cities:
            print('No cities found')
        if not clients:
            print('No clients found')
        return
    
    # Create fewer shipments for testing
    for i in range(1, shipments):
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
            updated_at=timezone.now() - timedelta(days=random.randint(0, 5))
        )
        
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




# Create data in the correct order
print('Starting data creation...')
create_superuser()
create_user(100)
create_company_profiles()
create_company_branches()
create_client(50)
create_driver(200)
create_branch(200)
create_recipient(200)
create_shipment(10000)
print('Data creation completed successfully!')
