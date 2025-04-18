from django.db import models

class TruckType(models.Model):
    name = models.CharField(max_length=100, verbose_name='نوع الشاحنة')
    description = models.TextField(verbose_name='الوصف', null=True, blank=True)

    class Meta:
        verbose_name = 'نوع الشاحنة'
        verbose_name_plural = 'أنواع الشاحنات'

    def __str__(self):
        return self.name  

class Driver(models.Model):
    name = models.CharField(max_length=255, verbose_name='اسم السائق')
    phone_number = models.CharField(max_length=20, verbose_name='رقم الهاتف')
    nationality = models.CharField(max_length=100, verbose_name='الجنسية')
    language = models.CharField(
        max_length=20, 
        choices=[('en', 'English'), ('ar', 'Arabic'), ('ur', 'Urdu')],
        default='en', 
        verbose_name='اللغة'
    )
    identity_number = models.CharField(max_length=20, verbose_name='رقم الهوية')
    vehicle_number = models.CharField(max_length=20, verbose_name='رقم المركبة')
    truck_type = models.ForeignKey(
        'TruckType',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='نوع الشاحنة'
    )

    status = models.CharField(
        max_length=10,
        choices=[
            ('available', 'Available'),
            ('busy', 'Busy'), 
            ('offline', 'Offline'),
        ],
        default='available',
        verbose_name='حالة السائق'
    )
    is_active = models.BooleanField(default=True, verbose_name='نشط')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاريخ التحديث')

    class Meta:
        verbose_name = 'سائق'
        verbose_name_plural = 'السائقين'

    def __str__(self):
        return self.name
