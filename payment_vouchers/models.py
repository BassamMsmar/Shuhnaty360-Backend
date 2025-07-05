from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

from shipments.models import Shipment, ShipmentStatus, ShipmentHistory
from clients.models import Client, Branch
from recipient.models import Recipient
from cities.models import City
from drivers.models import Driver
from profile_company.models import CompanyBranch
User = get_user_model()


PENDING = 'pending'
APPROVED = 'approved'
REJECTED = 'rejected'

APPROVAL_STATUS_CHOICES = [
    (PENDING, 'Pending'),
    (APPROVED, 'Approved'),
    (REJECTED, 'Rejected'),
]

# Create your models here.
class PaymentVoucher(models.Model):

    shipment = models.ForeignKey(
        Shipment,
        on_delete=models.CASCADE,
        related_name='payment_voucher',
        verbose_name='الشحنة المرتبطة'
    )

    tracking_number = models.CharField(
        "رقم الشحنة",
        max_length=50,
        unique=True,
        null=True,
        blank=True
    )

    driver = models.ForeignKey(
        Driver,
        on_delete=models.SET_NULL,
        null=True,
        related_name='payment_vouchers_driver',
        verbose_name='السائق'
    )

    tracking_number = models.CharField(
        "رقم التتبع",
        max_length=50,
        null=True,
        blank=True
    )
    origin_city = models.ForeignKey(
        City, on_delete=models.SET_NULL, related_name="origin_payment_vouchers", verbose_name="مدينة التحميل", null=True, blank=True
    )
    destination_city = models.ForeignKey(
        City, on_delete=models.SET_NULL, related_name="destination_payment_vouchers", verbose_name="مدينة الوجهة", null=True, blank=True
    )
    client = models.ForeignKey(
            Client,
            related_name='payment_vouchers_client',
            on_delete=models.SET_NULL,
            null=True
        )

    client_branch = models.ForeignKey(
        Branch,
        related_name='payment_vouchers_client_branch',
        on_delete=models.SET_NULL,
        null=True,
    )
    client_invoice_number = models.CharField(
            "Customer Invoice Number",
            max_length=50,  # قم بتحديد الطول المناسب حسب نظام الفواتير لديك
            null=True,
            blank=True
        )
    recipient = models.ForeignKey(
            Recipient,
            related_name='payment_vouchers_recipient',
            on_delete=models.SET_NULL,
            null=True
        )
    actual_delivery_date = models.DateTimeField(
            "تاريخ الوصول الفعلي", null=True, blank=True)
        
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
    approval_status = models.CharField(
        max_length=10,
        choices=APPROVAL_STATUS_CHOICES,
        default=PENDING,
        verbose_name='مستلم المبلغ'

    )
    reviewed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_payment_vouchers',
        verbose_name='مراجع السند'
    )
    rejection_reason = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='سبب الرفض'
    )
 
    receiver_name = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='received_payment_vouchers',
        verbose_name='مستلم المبلغ'

    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_payment_vouchers',
        verbose_name='منشئ السند'
    )

    issuing_branch = models.ForeignKey(
        CompanyBranch,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='issued_payment_vouchers',
        verbose_name="فرع الإصدار"
    )
    
 
    
    class Meta:
        verbose_name = "سند صرف"
        verbose_name_plural = "سندات الصرف"

    def __str__(self):
        return f"سند صرف #{self.pk}"

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
        super().save(*args, **kwargs)
