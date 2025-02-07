from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from drivers.models import Driver
from clients.models import Branch
import uuid

# Assuming the following models exist in your project:
# User, Driver, Branch, ShipmentStatus, City


# Create your models here.
class ShipmentStatus(models.Model):
    name_en = models.CharField( max_length=50, verbose_name='الحالة')
    name_ar = models.CharField( max_length=50, verbose_name='Status')

    def __str__(self):
        return self.name_en


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

    # Receiver (Customer's branch)
    customer_branch = models.ForeignKey(
        Branch,
        related_name='shipments_company',
        on_delete=models.SET_NULL,
        null=True
    )

    # Fare details
    fare = models.IntegerField("Fare")
    premium = models.IntegerField("Premium", null=True, blank=True)
    fare_return = models.IntegerField("Return", null=True, blank=True)

    # QR Code image for tracking
    code = models.ImageField(blank=True, null=True, upload_to='code')

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
    # Timestamps and notes
    created_at = models.DateTimeField("Created At", default=timezone.now)
    expected_arrival_date = models.DateTimeField(
        "Expected Arrival Date", null=True, blank=True, default=timezone.now)
    actual_delivery_date = models.DateTimeField(
        "Actual Delivery Date", null=True, blank=True, default=timezone.now)
    notes = models.TextField("Notes", null=True, blank=True)


    def save(self, *args, **kwargs):
        if not self.tracking_number:
            self.tracking_number = str(uuid.uuid4().int)[:10]  # رقم عشوائي مكون من 10 أرقام
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"Shipment {self.tracking_number}"

    class Meta:
        verbose_name = "Shipment"
        verbose_name_plural = "Shipments"
