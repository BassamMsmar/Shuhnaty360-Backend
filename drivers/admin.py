from django.contrib import admin
from .models import Driver
# Register your models here.



class DriverAdmin(admin.ModelAdmin):
    list_display = ('name', 'identity_number', 'nationality', 'vehicle_number', 'status')
    search_fields = ('name', 'identity_number', 'vehicle_number')

    
admin.site.register(Driver, DriverAdmin)
