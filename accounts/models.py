from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Create your models here.
class CustomUser(AbstractUser):
    phone = models.CharField(_('Phone'), max_length=100, blank=True, null=True)
    company_branch = models.ForeignKey(
        'profile_company.CompanyBranch',
        related_name='user_company_branch',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    email = models.EmailField(_('Email'), unique=True, blank=True, null=True)

    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name = _('User Profile')
        verbose_name_plural = _('User Profiles')