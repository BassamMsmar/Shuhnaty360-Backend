from django.contrib import admin
from .models import Shipment, ShipmentStatus, ShipmentHistory
# Register your models here.

class ShipmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'driver', 'client_branch', 'recipient', 'status', 'loading_at']
    list_filter = ['status', 'loading_at']
    search_fields = ['name', 'phone', 'address']

admin.site.register(Shipment, ShipmentAdmin )
admin.site.register(ShipmentStatus)
admin.site.register(ShipmentHistory)
