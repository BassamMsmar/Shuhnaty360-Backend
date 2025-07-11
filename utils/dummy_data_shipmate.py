import os
import django
import sys
import random
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# إعداد متغير البيئة لمشروع Django الخاص بك
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')  # استبدل 'project' باسم مشروعك الفعلي
django.setup()

from faker import Faker
from datetime import timedelta
from django.utils import timezone

from django.contrib.auth import get_user_model
User = get_user_model()

from cities.models import City
from clients.models import Client, Branch
from drivers.models import Driver
from recipient.models import Recipient
from shipments.models import Shipment, ShipmentStatus, ShipmentHistory


# Create shipments
def create_shipment():
    # Check if we already have shipments
    if Shipment.objects.count() > 100000000:
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
    for i in range(1, 1000000):
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
        
        # Create shipment history entries
        # create_shipment_history(shipment, statuses, users)
            
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

create_shipment()
create_shipment_history()
print('Data creation completed successfully!')
