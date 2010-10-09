from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from techism2.events.models import Event
from techism2.events.forms import EventForm
from datetime import datetime
from django.contrib.auth.decorators import login_required
from techism2.events import tag_cloud
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth import logout as django_logout

def index(request):
    tags = tag_cloud.get_tags()
    latest_event_list = Event.objects.filter(dateBegin__gte=datetime.today()).order_by('dateBegin')
    paginator = Paginator(latest_event_list, 25);
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
        
    try:
        latest_event_list = paginator.page(page)
    except (EmptyPage, InvalidPage):
        latest_event_list = paginator.page(paginator.num_pages)
    return render_to_response('events/index.html', {'latest_event_list': latest_event_list, 'tags': tags}, context_instance=RequestContext(request))

def detail(request, event_id):
    event = Event.objects.get(id=event_id)
    return render_to_response('events/detail.html', {'event':event}, context_instance=RequestContext(request))

def archive(request):
    event_list = Event.objects.filter(dateBegin__lt=datetime.today()).order_by('dateBegin')[:10]
    return render_to_response('events/archive.html', {'event_list' : event_list}, context_instance=RequestContext(request))

def impressum(request):
    return render_to_response('events/impressum.html', {}, context_instance=RequestContext(request))

def tag(request, tag_name):
    tags = tag_cloud.get_tags()
    event_list = Event.objects.filter(tags=tag_name)
    return render_to_response('events/tag.html', {'event_list': event_list, 'tag_name': tag_name, 'tags': tags}, context_instance=RequestContext(request))


@login_required
def create(request):
    if request.method == 'POST': 
        form = EventForm(request.POST) 
        if form.is_valid(): 
            event= __createEvent(form)
            event.save()
            return HttpResponseRedirect('/events/')
        else:
            return render_to_response('events/create.html', {'form': form, 'error': form.errors}, context_instance=RequestContext(request))
    form = EventForm ()
    return render_to_response('events/create.html', {'form': form}, context_instance=RequestContext(request))

def logout(request):
    django_logout(request)
    return HttpResponseRedirect('/')

def __createEvent (form):
    event = Event()
    event.title=form.cleaned_data['title']
    event.dateBegin=form.cleaned_data['dateBegin']
    event.dateEnd=form.cleaned_data['dateEnd']
    event.url=form.cleaned_data['url']
    event.description=form.cleaned_data['description']
    event.location=form.cleaned_data['location']
    event.tags=form.cleaned_data['tags']
    return event
