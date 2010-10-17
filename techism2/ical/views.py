from django.http import HttpResponse
from techism2 import service
from techism2.models import Event, Location
from datetime import datetime, timedelta
import icalendar
import time


def ical(request):
    ninety_days = datetime.utcnow() + timedelta(days=90)
    event_list = service.get_event_query_set().filter(date_time_begin__lte=ninety_days).order_by('date_time_begin')
    
    cal = icalendar.Calendar()
    cal['prodid'] = icalendar.vText(u'-//Techism//Techism//DE')
    cal['version'] = icalendar.vText(u'2.0')
    cal['x-wr-calname'] = icalendar.vText(u'Techism')
    cal['x-wr-caldesc'] = icalendar.vText(u'Techism - Open Source und Community Events in M\u00FCnchen')
    
    for e in event_list:
        event = icalendar.Event()
        
        # TODO should we generate an UUID when creating the event?
        uid = u'%s@techism.de' % (str(e.id))
        event['uid'] = icalendar.vText(uid)
        event['dtstamp'] = icalendar.vDatetime(datetime.utcnow())
        
        # The sequence field must be incremented each time the event is modifed.
        # The trick here is to subtract the create TS from the modify TS and 
        # use the difference as sequence.
        sequence = 0
        if e.date_time_created and e.date_time_modified:
            createTimestamp = time.mktime(e.get_date_time_created_utc().timetuple())
            modifyTimestamp = time.mktime(e.get_date_time_modified_utc().timetuple())
            sequence = modifyTimestamp - createTimestamp
        event['sequence'] = icalendar.vInt(sequence)
        
        # created and last-modified
        if e.date_time_created:
            event['created'] = icalendar.vDatetime(e.get_date_time_created_utc())
        if e.date_time_modified:
            event['last-modified'] = icalendar.vDatetime(e.get_date_time_modified_utc())
        
        # TENTATIVE, CONFIRMED, CANCELLED
        event['status'] = icalendar.vText(u'CONFIRMED')
        
        if e.title:
            event['summary'] = icalendar.vText(e.title)
        if e.description:
            event['description'] = icalendar.vText(e.description)
        if e.date_time_begin:
            event['dtstart'] = icalendar.vDatetime(e.get_date_time_begin_utc())
        if e.date_time_end:
            event['dtend'] = icalendar.vDatetime(e.get_date_time_end_utc())
        if e.url:
            event['url'] = icalendar.vUri(e.url)
        if e.location:
            location = u'%s, %s, %s' % (e.location.name, e.location.street, e.location.city)
            event['location'] = icalendar.vText(location)
        if e.location and e.location.latitude and e.location.longitude:
            event['geo'] = icalendar.vGeo((e.location.latitude, e.location.longitude))
        # TODO: remove hard-coded geo value
        event['geo'] = icalendar.vGeo((48.1372, 11.57542))
        
        cal.add_component(event)
    
    response = HttpResponse(cal.as_string())
    response['Content-Type'] = 'text/calendar; charset=UTF-8'
    response['Cache-Control'] = 'no-cache, no-store, max-age=0, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = 'Fri, 01 Jan 1990 00:00:00 GMT'
    return response

