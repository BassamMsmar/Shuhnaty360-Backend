from django.contrib import admin
from .models import Client, Branch


class BranchInline(admin.TabularInline):
    model = Branch
    extra = 1


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'email')
    search_fields = ('name', 'phone_number', 'email')
    inlines = [BranchInline]


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'client', 'phone_number')
    search_fields = ('name', 'client__name')
