from django import forms
from django.forms import ModelForm
from techism2.events.models import Event

class EventForm(ModelForm):
    class Meta:
        model = Event
        exclude = ['location']