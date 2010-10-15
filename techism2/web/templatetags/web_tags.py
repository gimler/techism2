from django.template import Library 
from django.template.defaultfilters import stringfilter
from datetime import date

register = Library()

@register.filter
def display_date(value):
    if not value:
        return '';
    elif (value.date()== date.today()):
        return "Heute"
    else:
        return value.strftime("%Y-%m-%d %H:%M")

