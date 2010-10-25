from django.http import HttpResponse
from techism2 import service
from datetime import datetime


def update_tags_cache(request):
    service.update_tags_cache()
    response = HttpResponse()
    return response

def update_archived_flag(request):
    content = []
    event_list = service.get_event_query_set().filter(date_time_begin__lte=datetime.utcnow()).order_by('date_time_begin')
    content.append(u'Processing %s events' % event_list.count())
    for event in event_list:
        __update_archived_flag(event, content)
    response = HttpResponse('\n'.join(content))
    return response

def __update_archived_flag(event, content):
    old_archived = event.archived
    event.update_archived_flag()
    # save only if archived flag has been changed
    if old_archived != event.archived:
        event.save()
        content.append(u'Modifed archive flag %s of event %s' % (event.archived, event.title))

