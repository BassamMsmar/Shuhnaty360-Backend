import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment_vouchers', '0003_remove_paymentvoucher_approved_by'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentvoucher',
            name='approval_status',
            field=models.CharField(choices=[('pending', 'قيد المراجعة'), ('approved', 'مقبول'), ('rejected', 'مرفوض')], default='pending', max_length=10, verbose_name='حالة السند'),
        ),
        migrations.AlterField(
            model_name='paymentvoucher',
            name='receiver_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='received_payment_vouchers', to=settings.AUTH_USER_MODEL, verbose_name='المستلم'),
        ),
    ]
