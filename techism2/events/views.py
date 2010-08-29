from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from techism2.events.models import Event
from techism2.events.forms import EventForm
from datetime import datetime
from django.contrib.auth.decorators import login_required

def index(request):
    latest_event_list = Event.objects.filter(dateBegin__gte=datetime.today()).order_by('dateBegin')[:10]
    return render_to_response('events/index.html', {'latest_event_list': latest_event_list}, context_instance=RequestContext(request))

def detail(request, event_id):
    event = Event.objects.get(id=event_id)
    return render_to_response('events/detail.html', {'event':event}, context_instance=RequestContext(request))

@login_required
def create(request):
    if request.method == 'POST': 
        form = EventForm(request.POST) 
        #if form.is_valid(): 
        return HttpResponseRedirect('/events/')
    form = EventForm ()
    return render_to_response('events/create.html', {'form': form}, context_instance=RequestContext(request))

