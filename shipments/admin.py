from django.contrib import admin
from .models import Shipment, ShipmentStatus, ShipmentHistory
# Register your models here.

class ShipmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'driver', 'client_branch', 'recipient', 'status', 'loading_date']
    list_filter = ['status', 'loading_date']
    search_fields = ['name', 'phone', 'address']

class ShipmentStatusAdmin(admin.ModelAdmin):
    list_display = ['id', 'name_ar', 'name_en']
    list_filter = ['name_ar', 'name_en']
    search_fields = ['name_ar', 'name_en']

class ShipmentHistoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'shipment', 'user', 'status', 'updated_at', 'notes']
    list_filter = ['shipment', 'user', 'status', 'updated_at', 'notes']
    search_fields = ['shipment', 'user', 'status', 'updated_at', 'notes']

admin.site.register(Shipment, ShipmentAdmin )
admin.site.register(ShipmentStatus, ShipmentStatusAdmin)
admin.site.register(ShipmentHistory, ShipmentHistoryAdmin)
