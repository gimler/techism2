#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from django.template import Library 
from django.conf import settings
from datetime import date, timedelta
import locale
from django.utils.translation import ugettext

register = Library()

@register.filter
def display_date(event_date):
    
    loc = settings.__getattr__('LANGUAGE_CODE')

    if not event_date:
        return '';
    elif (__is_today(event_date)):
        return "Heute, " + event_date.strftime("%H:%M")
    elif (__is_tomorrow(event_date)):
        return "Morgen, " + event_date.strftime("%H:%M")
    elif (__is_the_day_after_tomorrow(event_date)):
        
        return "Übermorgen, " + event_date.strftime("%H:%M")
    else:
        weekday = ugettext (event_date.strftime("%A"))[:2]
        day = event_date.day
        month = ugettext (event_date.strftime("%B"))[:3]
        time = event_date.strftime("%H:%M")
        return weekday + ", " + str(day) + ". " + month + " " + time
         
    

def __is_today(event_date):
    return event_date.date() == date.today()
    
def __is_tomorrow(event_date):
    return event_date.date() == date.today() + timedelta(days=1)
    
def __is_the_day_after_tomorrow(event_date):
    return event_date.date() == date.today() + timedelta(days=2)