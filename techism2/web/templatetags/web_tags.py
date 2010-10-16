 #!/usr/local/bin/python
 # -*- coding: utf-8 -*-
from django.template import Library 
from django.template.defaultfilters import stringfilter
from datetime import date, timedelta

register = Library()

@register.filter
def display_date(event_date):
    if not event_date:
        return '';
    elif (__is_today(event_date)):
        return "Heute, " + event_date.strftime("%H:%M")
    elif (__is_tomorrow(event_date)):
        return "Morgen, " + event_date.strftime("%H:%M")
    elif (__is_the_day_after_tomorrow(event_date)):
        return "Übermorgen, " + event_date.strftime("%H:%M")
    else:
        return event_date.strftime("%d. %b %Y %H:%M")
    

def __is_today(event_date):
    return event_date.date() == date.today()
    
def __is_tomorrow(event_date):
    return event_date.date() == date.today() + timedelta(days=1)
    
def __is_the_day_after_tomorrow(event_date):
    return event_date.date() == date.today() + timedelta(days=2)
