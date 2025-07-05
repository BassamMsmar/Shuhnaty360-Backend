from django.contrib import admin
from .models import PaymentVoucher

# Register your models here.
class PaymentVoucherAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_by', 'shipment_id_display', 'driver', 'issuing_branch', 'created_at']
    list_filter = ['issuing_branch', 'created_at', 'client']
    search_fields = ['shipment__tracking_number', 'id', 'driver', 'client_invoice_number']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related(
            "shipment",
            "shipment__status",
            "client",
            "client_branch",
            "driver",
            "recipient",
            "origin_city",
            "destination_city",
            "created_by",
            "reviewed_by",
            "receiver_name",
            "issuing_branch"
        )

    @admin.display(description="Shipment ID")
    def shipment_id_display(self, obj):
        return obj.shipment.id if obj.shipment else "-"

admin.site.register(PaymentVoucher, PaymentVoucherAdmin)

