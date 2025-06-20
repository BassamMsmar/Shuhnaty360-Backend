from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

from shipments.models import Shipment, ShipmentStatus, ShipmentHistory

User = get_user_model()

# Create your models here.
class PaymentVoucher(models.Model):

    shipment = models.OneToOneField(
        Shipment,
        on_delete=models.CASCADE,
        related_name='payment_voucher',
        verbose_name='الشحنة المرتبطة'
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_payment_vouchers',
        verbose_name='منشئ السند'
    )
    fare = models.IntegerField("Fare", null=True, blank=True)
    premium = models.IntegerField("Premium", null=True, blank=True)
    fare_return = models.IntegerField("Return", null=True, blank=True)
    days_stayed = models.IntegerField("Days Stayed", null=True, blank=True)
    stay_cost = models.IntegerField("Stay Cost", null=True, blank=True)
    deducted = models.IntegerField("Deducted", null=True, blank=True)

    
    note = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(
        'تاريخ الإنشاء',
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        'تاريخ التحديث',
        auto_now=True
    )
    
    class Meta:
        verbose_name = "سند صرف"
        verbose_name_plural = "سندات الصرف"

    def __str__(self):
        return f"سند صرف للشحنة {self.shipment.tracking_number}"

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
        super().save(*args, **kwargs)
        try:
            completed_status = ShipmentStatus.objects.get(name_ar="مكتملة")
        except ShipmentStatus.DoesNotExist:
            completed_status = None

        if completed_status and self.shipment.status.name_ar != "مكتملة":
            old_status = self.shipment.status
            self.shipment.status = completed_status
            self.shipment.save()

            ShipmentHistory.objects.create(
                shipment=self.shipment,
                old_status=old_status,
                new_status=completed_status,
                user=self.created_by,
                notes=self.note or f"تم إنشاء سند صرف للشحنة بواسطة {self.created_by.get_full_name()}" if self.created_by else "تم إنشاء سند صرف",
                action="PUT"
            )

