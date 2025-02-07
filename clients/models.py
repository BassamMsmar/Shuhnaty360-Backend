from django.db import models

# Create your models here.
from django.db import models

class Client(models.Model):
    name = models.CharField(max_length=255, verbose_name="اسم العميل")
    phone_number = models.CharField(max_length=20, verbose_name="رقم الهاتف")
    email = models.EmailField(unique=True, verbose_name="البريد الإلكتروني")
    address = models.TextField(verbose_name="العنوان", blank=True, null=True)

    class Meta:
        verbose_name = "عميل"
        verbose_name_plural = "العملاء"

    def __str__(self):
        return self.name


class Branch(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="branches", verbose_name="العميل")
    name = models.CharField(max_length=255, verbose_name="اسم الفرع")
    phone_number = models.CharField(max_length=20, verbose_name="رقم الهاتف")
    address = models.TextField(verbose_name="العنوان")
    city = models.CharField(max_length=100, verbose_name="المدينة")

    class Meta:
        verbose_name = "فرع"
        verbose_name_plural = "الفروع"

    def __str__(self):
        return f"{self.name} - {self.client.name}"
