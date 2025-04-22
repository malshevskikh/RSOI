from django.db import models

# Create your models here.

class Person(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(blank=True)
    address = models.CharField(blank=True, max_length=255)
    work = models.CharField(blank=True, max_length=255)

    def __str__(self):
        return self.name
