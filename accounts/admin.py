from django.contrib import admin
from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username',  'first_name', 'last_name',  'company_branch', 'is_superuser', 'is_staff','is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone', 'company_branch')
admin.site.register(CustomUser, CustomUserAdmin)


# Register your models here.
