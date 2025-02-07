from django.db import models
from cities.models import City

# Create your models here.
class Recipient(models.Model):
    name = models.CharField(max_length=255, verbose_name="اسم المستلم")
    city  = models.ForeignKey(City, on_delete=models.CASCADE, related_name="recipients", verbose_name="المدينة")
    address = models.CharField(verbose_name="العنوان",max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, verbose_name="رقم الهاتف", blank=True, null=True)
    email = models.EmailField(unique=True, verbose_name="البريد الإلكتروني", blank=True, null=True)

    class Meta:
        verbose_name = "مستلم"
        verbose_name_plural = "المستلمين"

    def __str__(self):
        return self.name
    
