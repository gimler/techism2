from django import forms
from django.forms import ModelForm
from techism2.events.models import Address

class EventForm(forms.Form):
    title = forms.CharField(max_length=200, label= 'Titel')
    dateBegin = forms.DateTimeField(label= 'Beginn')
    dateEnd = forms.DateTimeField(label= 'Ende',required=False)
    url = forms.URLField()
    description = forms.CharField(label= 'Beschreibung', widget=forms.Textarea )
    location = forms.ModelChoiceField (Address.objects.all(), required=False)
    
    #name = forms.CharField(max_length=200, required=False)
    #street = forms.CharField(max_length=200, required=False)
    #city = forms.CharField(max_length=200,required=False)
    #latitude = forms.FloatField(required=False)
    #longitude = forms.FloatField(required=False)
  