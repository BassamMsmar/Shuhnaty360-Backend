from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'phone', 'company_branch', 'password1', 'password2')

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    list_display = ('id', 'username',  'first_name', 'last_name',  'company_branch', 'is_superuser', 'is_staff','is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone', 'company_branch')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone', 'company_branch')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'phone', 'company_branch', 'password1', 'password2'),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
