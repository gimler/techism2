from django.db import models

class Event(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField('event date')
    url = models.URLField()
    description = models.CharField(max_length=2000)
