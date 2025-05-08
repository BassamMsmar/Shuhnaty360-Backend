from django.db import models
from cities.models import City


class CompanyProfile(models.Model):
    company_name_ar = models.CharField(max_length=255, verbose_name='اسم الشركة', null=True, blank=True)
    company_name_en = models.CharField(max_length=255, verbose_name='Company Name', null=True, blank=True)
    company_logo = models.ImageField(upload_to='company_logos/', null=True, blank=True)
    company_description_ar = models.TextField(verbose_name='وصف الشركة', null=True, blank=True)
    company_description_en = models.TextField(verbose_name='Company Description', null=True, blank=True)
    main_phone_number = models.CharField(max_length=20, verbose_name='الرقم الأساسي', null=True, blank=True)
    secondary_phone_number = models.CharField(max_length=20, verbose_name='الرقم الفرعي', null=True, blank=True)
    email = models.EmailField(verbose_name='البريد الالكتروني', null=True, blank=True)
    website = models.URLField(verbose_name='الموقع الالكتروني', null=True, blank=True)
    address = models.TextField(verbose_name='العنوان', null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = ' ملف شركة '
        verbose_name_plural = 'بيانات الشركة'

    def __str__(self):
        return self.company_name_ar or 'ملف شركة جديد'



class CompanyBranch(models.Model):
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE, related_name='branches')
    branch_name_ar = models.CharField(max_length=255, verbose_name='اسم الفرع', null=True, blank=True)
    branch_name_en = models.CharField(max_length=255, verbose_name='Branch Name', null=True, blank=True)
    main_phone_number = models.CharField(max_length=20, verbose_name='الرقم الأساسي', null=True, blank=True)
    secondary_phone_number = models.CharField(max_length=20, verbose_name='الرقم الفرعي', null=True, blank=True)
    email = models.EmailField(verbose_name='البريد الالكتروني', null=True, blank=True)
    address = models.TextField(verbose_name='العنوان', null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = ' الفرع'
        verbose_name_plural = ' الفروع '

    def __str__(self):
        return self.branch_name_ar or 'فرع جديد'

