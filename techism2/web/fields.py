from django import forms

class CommaSeparatedListWidget(forms.TextInput):
    def render(self, name, value, attrs=None):
        if isinstance(value, (list, tuple)):
            value = u', '.join([unicode(v) for v in value])
        return super(CommaSeparatedListWidget, self).render(name, value, attrs)
    
class CommaSeparatedListFormField(forms.Field):
    widget = CommaSeparatedListWidget
    def clean(self, value):
        return [v.strip() for v in value.split(',') if len(v.strip()) > 0]
