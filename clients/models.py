from django.db import models

from cities.models import City


class Client(models.Model):
    name = models.CharField(max_length=255, verbose_name="اسم العميل")
    address = models.CharField(
        verbose_name="العنوان", max_length=255, blank=True, null=True)
    phone_number = models.CharField(
        max_length=20, verbose_name="رقم الهاتف", null=True, blank=True)
    second_phone_number = models.CharField(max_length=20, verbose_name="رقم الهاتف الثاني", null=True, blank=True)
    email = models.EmailField(
        unique=True, verbose_name="البريد الإلكتروني", null=True, blank=True)
    Commercial_registration_number = models.CharField(
        max_length=50, verbose_name="رقم السجل التجاري", null=True, blank=True)
    dicription = models.TextField(
        verbose_name="وصف", blank=True, null=True)

    class Meta:
        verbose_name = "عميل"
        verbose_name_plural = "العملاء"

    def __str__(self):
        return self.name


class Branch(models.Model):
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="branches", verbose_name="العميل")
    name = models.CharField(max_length=255, verbose_name="اسم الفرع")
    city = models.ForeignKey(
        City, on_delete=models.CASCADE, related_name="clients", verbose_name="المدينة")
        
    address = models.CharField(verbose_name="العنوان", max_length=255)
    
    name_address = models.CharField(
        verbose_name="اسم العنوان", max_length=255, blank=True, null=True)
    
    phone_number = models.CharField(
        max_length=20, verbose_name="رقم الهاتف",  null=True, blank=True)
    
    second_phone_number = models.CharField(
        max_length=20, verbose_name="رقم الهاتف الثاني",  null=True, blank=True)

    class Meta:
        verbose_name = "فرع"
        verbose_name_plural = "الفروع"

    def __str__(self):
        return f"{self.name} - {self.client.name}"
