from statistics import mode
from django.db import models

# Create your models here.

class Urls(models.Model):
    suffix = models.CharField(max_length=20)
    url = models.CharField(max_length=10000)