from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

from clients.models import Client, Branch

# Create your models here.


class profile (models.Model):
    user = models.OneToOneField(
        User, related_name='profile', on_delete=models.CASCADE)
    phone = models.CharField(max_length=100, blank=True, null=True)
    branch = models.ForeignKey(
        Branch, related_name='user_branch', on_delete=models.SET_NULL, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.first_name

    class Meta:
        verbose_name = 'صفجة المستخدم'
        verbose_name_plural = 'صفحات المستخدمين'


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        profile.objects.create(user=instance)
