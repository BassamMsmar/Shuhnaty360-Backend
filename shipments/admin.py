from django.contrib import admin
from .models import Shipment, ShipmentStatus, ShipmentHistory
# Register your models here.

class ShipmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'tracking_number', 'driver', 'client_branch', 'recipient', 'status', 'loading_date']
    list_filter = ['status', 'loading_date']
    search_fields = ['tracking_number', 'client_invoice_number']

class ShipmentStatusAdmin(admin.ModelAdmin):
    list_display = ['id', 'name_ar', 'name_en']
    list_filter = ['name_ar', 'name_en']
    search_fields = ['name_ar', 'name_en']

class ShipmentHistoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'shipment_id', 'user', 'old_status', 'new_status', 'action', 'updated_at', 'notes']
    list_filter = ['shipment', 'user', 'old_status', 'new_status', 'action', 'updated_at']
    search_fields = ['shipment__id', 'user__username', 'old_status__name_ar', 'new_status__name_ar', 'action', 'notes']
    
    def shipment_id(self, obj):
        return obj.shipment.id if obj.shipment else None
    shipment_id.short_description = 'Shipment ID'
    shipment_id.admin_order_field = 'shipment__id'

admin.site.register(Shipment, ShipmentAdmin )
admin.site.register(ShipmentStatus, ShipmentStatusAdmin)
admin.site.register(ShipmentHistory, ShipmentHistoryAdmin)
