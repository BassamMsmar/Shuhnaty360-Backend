from django.contrib import admin
from .models import CompanyProfile, CompanyBranch

# Register your models here.

class BranchInline(admin.TabularInline):
    model = CompanyBranch
    extra = 1

@admin.register(CompanyProfile)
class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = ('company_name_ar', 'company_name_en', 'city')
    search_fields = ('company_name_ar', 'company_name_en')
    inlines = [BranchInline]

@admin.register(CompanyBranch)
class CompanyBranchAdmin(admin.ModelAdmin):
    list_display = ('branch_name_ar', 'branch_name_en', 'company')
    search_fields = ('branch_name_ar', 'branch_name_en')
