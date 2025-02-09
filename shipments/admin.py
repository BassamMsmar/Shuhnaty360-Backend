from django.contrib import admin
from .models import Shipment, ShipmentStatus
# Register your models here.

class ShipmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'driver', 'customer_branch', 'recipient', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'phone', 'address']

admin.site.register(Shipment, ShipmentAdmin )
admin.site.register(ShipmentStatus)
