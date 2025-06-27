from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model

from drivers.models import Driver, TruckType
from clients.models import Branch, Client
from recipient.models import Recipient
from cities.models import City
import uuid


User = get_user_model()
# Assuming the following models exist in your project:
# User, Driver, Branch, ShipmentStatus, City


# Create your models here.
class ShipmentStatus(models.Model):
    name_ar = models.CharField(max_length=50, verbose_name='الحالة')
    name_en = models.CharField(max_length=50, verbose_name='Status')

    def __str__(self):
        return self.name_ar
    
    class Meta:
        verbose_name = "حالة الشحنة"
        verbose_name_plural = "حالات الشحنات"


class Shipment(models.Model):
    tracking_number = models.CharField(max_length=20, unique=True, editable=False, blank=True, null=True)

    # Sender (User)
    user = models.ForeignKey(
        User,
        related_name='shipments_user',
        on_delete=models.SET_NULL,
        null=True
    )

    # Assigned driver
    driver = models.ForeignKey(
        Driver,
        related_name='shipments_driver',
        on_delete=models.SET_NULL,
        null=True
    )
    truck_type = models.ForeignKey(
        TruckType,
        related_name='shipments_truck_type',
        on_delete=models.SET_NULL,
        null=True
    )
    vehicle_number = models.CharField(
        max_length=20, verbose_name='رقم المركبة' , null=True, blank=True
    )
    driver_phone_number = models.CharField(
        max_length=20, verbose_name='رقم هاتف السائق' , null=True, blank=True
    )
    
    # Receiver (Customer's branch)
    client = models.ForeignKey(
        Client,
        related_name='shipments_customer',
        on_delete=models.SET_NULL,
        null=True
    )


    client_branch = models.ForeignKey(
        Branch,
        related_name='shipments_company',
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={'client': models.F('client')}
    )

    client_invoice_number = models.CharField(
        "Customer Invoice Number",
        max_length=50,  # قم بتحديد الطول المناسب حسب نظام الفواتير لديك
        null=True,
        blank=True
    )
    notes_customer = models.TextField("ملاحظات العميل", null=True, blank=True)

    # Recipient details
    recipient = models.ForeignKey(
        Recipient,
        related_name='shipments_recipient',
        on_delete=models.SET_NULL,
        null=True
    )
    notes_recipient = models.TextField("ملاحظات المستلم", null=True, blank=True)

    # Fare details
    fare = models.IntegerField("Fare")
    premium = models.IntegerField("Premium", null=True, blank=True)
    fare_return = models.IntegerField("Return", null=True, blank=True)

    origin_city = models.ForeignKey(
        City, on_delete=models.SET_NULL, related_name="origin_shipments", verbose_name="مدينة التحميل", null=True, blank=True
    )
    destination_city = models.ForeignKey(
        City, on_delete=models.SET_NULL, related_name="destination_shipments", verbose_name="مدينة الوجهة", null=True, blank=True
    )

    # Additional shipment details
    days_stayed = models.IntegerField("Days Stayed", null=True, blank=True)
    stay_cost = models.IntegerField("Stay Cost", null=True, blank=True)
    deducted = models.IntegerField("Deducted", null=True, blank=True)

    # Shipment status
    status = models.ForeignKey(
        ShipmentStatus,
        verbose_name="الحالة",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    loading_date = models.DateTimeField("تاريخ التحميل", null=True, blank=True)
    days_to_arrive = models.IntegerField("عدد الأيام  الوصول", null=True, blank=True, default=3)
    expected_arrival_date = models.DateTimeField(
        "تاريخ الوصول المتوقع", null=True, blank=True) # 
    
    actual_delivery_date = models.DateTimeField(
        "تاريخ الوصول الفعلي", null=True, blank=True)
    
    weight = models.FloatField("وزن الشحنة (طن)", null=True, blank=True)
    contents = models.TextField("محتويات الشحنة", null=True, blank=True)
    
    notes = models.TextField("ملاحظات", null=True, blank=True)

    # Timestamps and notes
    created_at = models.DateTimeField("تاريخ الانشاء", default=timezone.now)
    updated_at = models.DateTimeField("تاريخ التحديث", auto_now=True)


    @property
    def total_cost(self):
        """حساب التكلفة الإجمالية للشحنة"""
        fare = self.fare or 0
        premium = self.premium or 0
        deducted = self.deducted or 0
        days_stayed = self.days_stayed or 0
        stay_cost = self.stay_cost or 0
        fare_return = self.fare_return or 0
        return fare + premium - deducted + (stay_cost * days_stayed) + fare_return



    def save(self, *args, **kwargs):
        days_to_arrive = self.days_to_arrive
        if days_to_arrive:
            self.expected_arrival_date = timezone.now() + timedelta(days=days_to_arrive)

        if not self.tracking_number:
            self.tracking_number = str(uuid.uuid4().int)[:10]  # رقم عشوائي مكون من 10 أرقام

        super().save(*args, **kwargs)
        

    def save(self, *args, **kwargs):
        if not self.tracking_number:
            self.tracking_number = self.generate_tracking_number()
        super().save(*args, **kwargs)

    def generate_tracking_number(self):
        # توليد رقم تتبع فريد (مثلاً: SHIP-ABC1234567)
        return f'{uuid.uuid4().hex[:10].upper()}'

    def __str__(self):
        return f"Shipment {self.id} - {self.tracking_number}"
    

    class Meta:
        verbose_name = "الشحنه"
        verbose_name_plural = "الشحنات"

class ShipmentHistory(models.Model):
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE, related_name='history')
    old_status = models.ForeignKey(ShipmentStatus, on_delete=models.SET_NULL, null=True, blank=True, related_name='old_histories')
    new_status = models.ForeignKey(ShipmentStatus, on_delete=models.SET_NULL, null=True, blank=True, related_name='new_histories')
    action = models.CharField(max_length=10, default='PUT')  # Since it's an update view
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        user_name = self.user.get_full_name() if self.user else "مستخدم غير معروف"
        old = self.old_status.name_ar if self.old_status else "بدون حالة"
        new = self.new_status.name_ar if self.new_status else "بدون حالة"
        shipment_number = self.shipment.tracking_number
        date = self.updated_at.strftime('%Y-%m-%d %H:%M')
        return f"قام {user_name} بتحديث حالة الشحنة رقم {shipment_number} من '{old}' إلى '{new}' بتاريخ {date}"

    class Meta:
        verbose_name = "تاريخ الشحنه"
        verbose_name_plural = "تواريخ الشحنات"