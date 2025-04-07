from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
from drivers.models import Driver
from clients.models import Branch
from recipient.models import Recipient
from cities.models import City
import uuid

import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image

# Assuming the following models exist in your project:
# User, Driver, Branch, ShipmentStatus, City


# Create your models here.
class ShipmentStatus(models.Model):
    name_en = models.CharField( max_length=50, verbose_name='الحالة')
    name_ar = models.CharField( max_length=50, verbose_name='Status')

    def __str__(self):
        return self.name_en
    
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

    # Receiver (Customer's branch)
    customer_branch = models.ForeignKey(
        Branch,
        related_name='shipments_company',
        on_delete=models.SET_NULL,
        null=True
    )

    customer_invoice_number = models.CharField(
        "Customer Invoice Number",
        max_length=50,  # قم بتحديد الطول المناسب حسب نظام الفواتير لديك
        null=True,
        blank=True
    )



    # Recipient details
    recipient = models.ForeignKey(
        Recipient,
        related_name='shipments_recipient',
        on_delete=models.SET_NULL,
        null=True
    )

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
    updated_at = models.DateTimeField("Updated At", auto_now=True)

    days_to_arrive = models.IntegerField("Days to Arrive", null=True, blank=True, default=3)
    expected_arrival_date = models.DateTimeField(
        "Expected Arrival Date", null=True, blank=True)
    
    actual_delivery_date = models.DateTimeField(
        "Actual Delivery Date", null=True, blank=True)
    
    notes = models.TextField("Notes", null=True, blank=True)


    def save(self, *args, **kwargs):
        days_to_arrive = self.days_to_arrive
        if days_to_arrive:
            self.expected_arrival_date = timezone.now() + timedelta(days=days_to_arrive)

        if not self.tracking_number:
            self.tracking_number = str(uuid.uuid4().int)[:10]  # رقم عشوائي مكون من 10 أرقام

        # if not self.code:
        # # Generate QR code
        #     qr = qrcode.QRCode(
        #         version=1,
        #         error_correction=qrcode.constants.ERROR_CORRECT_L,
        #         box_size=4,
        #         border=4,
        #     )
        #     qr.add_data(f'http://127.0.0.1:8000/shipment/{self.id}/')
        #     qr.make(fit=True)

        #     img = qr.make_image(fill_color="black", back_color="white")

        #     # Save QR code to image field
        #     buffer = BytesIO()
        #     img.save(buffer, format='PNG')
        #     self.code.save(f'{self.id}_qrcode.png', File(buffer), save=False)

        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"Shipment {self.tracking_number}"

    class Meta:
        verbose_name = "الشحنه"
        verbose_name_plural = "الشحنات"
