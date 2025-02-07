
from django.db import models


class City(models.Model):
    ar_city = models.CharField(
        max_length=255, unique=True, verbose_name="المدينة")
    en_city = models.CharField(
        max_length=255, unique=True, verbose_name="City")

    def __str__(self):
        return self.ar_city
