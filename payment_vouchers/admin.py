from django.contrib import admin
from .models import PaymentVoucher

# Register your models here.
class PaymentVoucherAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_by','shipment__id', 'driver', 'issuing_branch', 'created_at']
    list_filter = ['issuing_branch', 'created_at', 'client']
    search_fields = ['shipment__tracking_number', 'id', 'driver', 'client_invoice_number']
admin.site.register(PaymentVoucher, PaymentVoucherAdmin)

