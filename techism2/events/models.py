from django.db import models

class Address(models.Model):
    name = models.CharField(max_length=200)
    street = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    
class Event(models.Model):
    title = models.CharField(max_length=200)
    dateBegin = models.DateField('event date from')
    dateEnd = models.DateField('event date to', blank=True, null=True)
    url = models.URLField()
    description = models.TextField()
    location = models.ForeignKey(Address, blank=True, null=True)
    
    

