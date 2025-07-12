from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    phone = models.CharField(max_length=100, blank=True, null=True)
    company_branch = models.ForeignKey(
        to='profile_company.CompanyBranch',
        related_name='user_company_branch',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    email = models.EmailField(unique=True, blank=True, null=True)

    class Meta:
        verbose_name = 'المستخدم'
        verbose_name_plural = 'المستخدمين'

    def __str__(self):
        return self.username
    
    def get_full_name(self):
        return self.first_name + ' ' + self.last_name