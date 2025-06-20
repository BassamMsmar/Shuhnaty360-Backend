from django.contrib import admin
from .models import PaymentVoucher

# Register your models here.
class PaymentVoucherAdmin(admin.ModelAdmin):
    list_display = ['id', 'shipment', 'note', 'updated_at', 'created_at']
    list_filter = ['shipment', 'updated_at', 'created_at']
    search_fields = ['shipment__tracking_number', 'note']
admin.site.register(PaymentVoucher, PaymentVoucherAdmin)

