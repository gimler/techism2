 #!/usr/local/bin/python
 # -*- coding: utf-8 -*-
from pytz.gae import pytz
from pytz import timezone

utc = pytz.utc
cet = timezone('Europe/Berlin')

def cet_to_utc (cet_datetime):
    if cet_datetime == None:
        return None
    localized = cet.localize(cet_datetime)
    utc_datetime = localized.astimezone(utc)
    return utc_datetime

def utc_to_cet (utc_datetime):
    if utc_datetime == None:
        return None
    localized = utc.localize(utc_datetime)
    cet_datetime = localized.astimezone(cet)
    return cet_datetime

def localize_to_utc (datetime):
    if datetime == None:
        return None
    if datetime.tzinfo == None:
        localized = utc.localize(datetime)
        return localized
    else:
        utc_datetime = datetime.astimezone(utc)
        return utc_datetime
