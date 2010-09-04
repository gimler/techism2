from django.db import models
from techism2.events import fields

class Address(models.Model):
    name = models.CharField(max_length=200)
    street = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    
    def __unicode__(self):
        return self.name;
    
class Event(models.Model):
    title = models.CharField(max_length=200)
    dateBegin = models.DateField()
    dateEnd = models.DateField(blank=True, null=True)
    url = models.URLField()
    description = models.TextField()
    location = models.ForeignKey(Address, blank=True, null=True)
    tags = fields.CommaSeparatedListField(models.CharField(max_length=20), blank=True, null=True)
    
    def __unicode__(self):
        return self.title
    
    

