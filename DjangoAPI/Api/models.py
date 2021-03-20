from django.db import models

# Create your models here.

class MyFile(models.Model):
    image = models.ImageField()