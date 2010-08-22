from django.shortcuts import render_to_response
from techism2.events.models import Event
from django.http import HttpResponse

def index(request):
    latest_event_list = Event.objects.all().order_by('-dateBegin')[:10]
    return render_to_response('events/index.html', {'latest_event_list': latest_event_list})

def detail(request, event_id):
    event = Event.objects.get(id=event_id);
    return render_to_response('events/detail.html', {'event':event})

def results(request, event_id):
    return HttpResponse("You're looking at the results of event %s." % event_id)

