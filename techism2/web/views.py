from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.http import HttpResponseForbidden
from techism2.models import Event, Location
from techism2.web.forms import EventForm
from datetime import datetime
from techism2 import service
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth import logout as django_logout


def index(request):
    tags = service.get_tags()
    event_list = Event.objects.filter(date_time_begin__gte=datetime.today()).order_by('date_time_begin')
    
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    
    paginator = Paginator(event_list, 10);
    try:
        event_list = paginator.page(page)
    except (EmptyPage, InvalidPage):
        event_list = paginator.page(paginator.num_pages)
    
    return render_to_response('events/index.html', {'event_list': event_list, 'tags': tags}, context_instance=RequestContext(request))

def archive(request):
    event_list = Event.objects.filter(dateTimeBegin__lt=datetime.today()).order_by('dateTimeBegin')[:10]
    return render_to_response('events/archive.html', {'event_list' : event_list}, context_instance=RequestContext(request))

def impressum(request):
    return render_to_response('events/impressum.html', {}, context_instance=RequestContext(request))

def tag(request, tag_name):
    tags = service.get_tags()
    event_list = Event.objects.filter(tags=tag_name)
    return render_to_response('events/tag.html', {'event_list': event_list, 'tag_name': tag_name, 'tags': tags}, context_instance=RequestContext(request))

def create(request):
    if request.method == 'POST': 
        form = EventForm(request.POST) 
        if form.is_valid(): 
            event= __createEvent(form, request.user)
            if event.location == None:
                location=__createLocation(form)
                location.save()
                event.location=location
            event.save()
            return HttpResponseRedirect('/events/')
        else:
            return render_to_response(
                'events/event.html',
                {
                    'form': form, 
                    'error': form.errors,
                    'button_label': u'Event hinzuf\u00FCgen'
                },
                context_instance=RequestContext(request))
    form = EventForm ()
    return render_to_response(
        'events/event.html',
        {
            'form': form,
            'button_label': u'Event hinzuf\u00FCgen'
        },
        context_instance=RequestContext(request))

def edit(request, event_id):
    event = Event.objects.get(id=event_id)
    if event.user != request.user and request.user.is_superuser == False:
        return HttpResponseForbidden()

    if request.method == 'POST': 
        form = EventForm(request.POST) 
        if form.is_valid(): 
            event= __editEvent(form, event)
            # TODO: handle location modification
            event.save()
            return HttpResponseRedirect('/events/')
        else:
            return render_to_response(
                'events/event.html',
                {
                    'form': form, 
                    'error': form.errors,
                    'button_label': u'Event \u00E4ndern'
                },
                context_instance=RequestContext(request))

    form = __toEventForm(event)
    return render_to_response(
        'events/event.html',
        {
            'form': form,
            'button_label': u'Event \u00E4ndern'
        },
        context_instance=RequestContext(request))


def logout(request):
    django_logout(request)
    return HttpResponseRedirect('/')

def __createEvent (form, user):
    event = Event()
    event.title=form.cleaned_data['title']
    event.set_date_time_begin_cet(form.cleaned_data['date_time_begin'])
    event.set_date_time_end_cet(form.cleaned_data['date_time_end'])
    event.url=form.cleaned_data['url']
    event.description=form.cleaned_data['description']
    event.location=form.cleaned_data['location']
    event.tags=form.cleaned_data['tags']
    if user.is_authenticated():
        event.user=user
    return event

def __editEvent (form, event):
    event.title=form.cleaned_data['title']
    event.set_date_time_begin_cet(form.cleaned_data['date_time_begin'])
    event.set_date_time_end_cet(form.cleaned_data['date_time_end'])
    event.url=form.cleaned_data['url']
    event.description=form.cleaned_data['description']
    event.tags=form.cleaned_data['tags']
    return event

def __createLocation (form):
    location = Location()
    location.name=form.cleaned_data['location_name']
    location.street=form.cleaned_data['location_street']
    location.city=form.cleaned_data['location_city']
    return location

def __toEventForm (event):
    data = {'title': event.title,
            'date_time_begin': event.get_date_time_begin_cet(),
            'date_time_begin_0': event.get_date_time_begin_cet(),
            'date_time_begin_1': event.get_date_time_begin_cet(),
            'date_time_end': event.get_date_time_end_cet(),
            'date_time_end_0': event.get_date_time_end_cet(),
            'date_time_end_1': event.get_date_time_end_cet(),
            'url': event.url,
            'description': event.description,
            'location': event.location.id,
            'tags': event.tags,
            #'location_name': event.location.name,
            #'location_street': event.location.street,
            #'location_city': event.location.city
            }
    form = EventForm(data)
    return form;


