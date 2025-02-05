from django.db import models

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

    class Meta:
        verbose_name = 'سائق'
        verbose_name_plural = 'السائقين'

    def __str__(self):
        return self.name
