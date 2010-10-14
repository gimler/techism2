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

    def clean(self):
        cleaned_data = self.cleaned_data
        location_name = cleaned_data.get("location_name")
        location_street = cleaned_data.get("location_street")
        location_city = cleaned_data.get("location_city")
        
        if location_name or location_street or location_city:
            if not location_name:
                self._errors["location_name"] = self.error_class([u'Alle Location Felder m\u00FCssen gef\u00FCllt sein.'])
                del cleaned_data["location_name"]
            if not location_street:
                self._errors["location_street"] = self.error_class([u'Alle Location Felder m\u00FCssen gef\u00FCllt sein.'])
                del cleaned_data["location_street"]
            if not location_city:
                self._errors["location_city"] = self.error_class([u'Alle Location Felder m\u00FCssen gef\u00FCllt sein.'])
                del cleaned_data["location_city"]
        
        return cleaned_data 