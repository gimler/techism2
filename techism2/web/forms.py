from django import forms
from django.forms import ModelForm
from techism2.models import Location
from techism2.models import Event
from techism2.web import fields


class EventForm(forms.Form):
    title = forms.CharField(max_length=200, label='Titel')
    dateTimeBegin = forms.SplitDateTimeField(label='Beginn', widget=forms.SplitDateTimeWidget(date_format='%Y-%m-%d', time_format='%H:%M'))
    dateTimeEnd = forms.SplitDateTimeField(label='Ende', required=False, widget=forms.SplitDateTimeWidget(date_format='%Y-%m-%d', time_format='%H:%M'))
    url = forms.URLField()
    description = forms.CharField(label= 'Beschreibung', widget=forms.Textarea )
    location = forms.ModelChoiceField (Location.objects.all(), required=False)
    tags = fields.CommaSeparatedListFormField(label= 'Tags', required=False)
    
    location_name = forms.CharField(label= 'Name',max_length=200, required=False)
    location_street = forms.CharField(label= 'Strasse & Hausnr.',max_length=200, required=False)
    location_city = forms.CharField(label= 'Ort', max_length=200,required=False)
    #latitude = forms.FloatField(required=False)
    #longitude = forms.FloatField(required=False)
  