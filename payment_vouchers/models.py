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
    creator = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_payment_vouchers',
        verbose_name='منشئ السند'
    )
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

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.shipment.status.name_ar == "مكتملة":
            completed_status = ShipmentStatus.objects.get(name_ar="مكتملة")
            self.shipment.status = completed_status
            self.shipment.save()
            
            # إنشاء سجل في التاريخ
            ShipmentHistory.objects.create(
                shipment=self.shipment,
                status=completed_status,
                user=self.creator,
                notes=self.note,
                updated_at=self.updated_at
            )

    def update_status(self, user, notes):
        self.updated_at = timezone.now()
        self.save()
        
        ShipmentHistory.objects.create(
            shipment=self.shipment,
            status=self.shipment.status,
            user=user,
            notes=notes,
            updated_at=self.updated_at
        )
