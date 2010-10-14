from djangotoolbox import fields

class CommaSeparatedListField(fields.ListField):
    def formfield(self, **kwargs):
        defaults = {'form_class': CommaSeparatedListFormField}
        defaults.update(kwargs)
        return super(fields.ListField, self).formfield(**defaults)
