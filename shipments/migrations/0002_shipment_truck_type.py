
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drivers', '0001_initial'),
        ('shipments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shipment',
            name='truck_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='shipments_truck_type', to='drivers.trucktype'),
        ),
    ]
