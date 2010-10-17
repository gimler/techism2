from django import forms
from djangotoolbox import fields

class CommaSeparatedListField(fields.ListField):
    def formfield(self, **kwargs):
        defaults = {'form_class': CommaSeparatedListFormField}
        defaults.update(kwargs)
        return super(fields.ListField, self).formfield(**defaults)

class CommaSeparatedListWidget(forms.TextInput):
    def render(self, name, value, attrs=None):
        if isinstance(value, (list, tuple)):
            value = u', '.join([unicode(v) for v in value])
        return super(CommaSeparatedListWidget, self).render(name, value, attrs)
    
class CommaSeparatedListFormField(forms.Field):
    widget = CommaSeparatedListWidget
    def clean(self, value):
        return [v.strip() for v in value.split(',') if len(v.strip()) > 0]
