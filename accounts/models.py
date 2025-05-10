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

    # Add related_names to override default reverse accessors
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )

    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name = 'المستخدم'
        verbose_name_plural = 'المستخدمين'