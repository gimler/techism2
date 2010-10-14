from django import forms
from django.forms import ModelForm
from techism2.models import Location
from techism2.models import Event
from techism2.web import fields


class EventForm(forms.Form):
    title = forms.CharField(max_length=200, label=u'Titel')
    date_time_begin = forms.SplitDateTimeField(label=u'Beginn', widget=forms.SplitDateTimeWidget(date_format='%Y-%m-%d', time_format='%H:%M'))
    date_time_end = forms.SplitDateTimeField(label=u'Ende', required=False, widget=forms.SplitDateTimeWidget(date_format='%Y-%m-%d', time_format='%H:%M'))
    url = forms.URLField()
    description = forms.CharField(label= u'Beschreibung', widget=forms.Textarea )
    location = forms.ModelChoiceField (Location.objects.all(), required=False)
    tags = fields.CommaSeparatedListFormField(label= u'Tags', required=False)
    
    location_name = forms.CharField(label= u'Name',max_length=200, required=False)
    location_street = forms.CharField(label= u'Stra\u00DFe & Hausnr.',max_length=200, required=False)
    location_city = forms.CharField(label= u'Ort', max_length=200,required=False)
    #latitude = forms.FloatField(required=False)
    #longitude = forms.FloatField(required=False)
  