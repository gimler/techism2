from django import forms
from django.forms import ModelForm
from techism2.events.models import Address
from techism2.events import fields

class EventForm(forms.Form):
    title = forms.CharField(max_length=200, label= 'Titel')
    dateBegin = forms.DateTimeField(label= 'Beginn')
    dateEnd = forms.DateTimeField(label= 'Ende',required=False)
    url = forms.URLField()
    description = forms.CharField(label= 'Beschreibung', widget=forms.Textarea )
    location = forms.ModelChoiceField (Address.objects.all(), required=False)
    tags = fields.CommaSeparatedListFormField(label= 'Tags', required=False)
    
    location_name = forms.CharField(label= 'Name',max_length=200, required=False)
    location_street = forms.CharField(label= 'Strasse & Hausnr.',max_length=200, required=False)
    location_city = forms.CharField(label= 'Ort', max_length=200,required=False)
    #latitude = forms.FloatField(required=False)
    #longitude = forms.FloatField(required=False)
  