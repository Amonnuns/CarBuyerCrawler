from django.db import models

class Car(models.Model):
    name = models.CharField(max_length=200)
    price = models.CharField(max_length=20,blank=True, null=True)
    mileage = models.CharField(max_length=20,blank=True, null=True)
    exchange = models.CharField(max_length=30, blank=True, null=True)
    url = models.TextField(null=True)
    img = models.TextField(null=True)

class Meta:
    db_table = 'Car'

def __str__(self):
    return self.name