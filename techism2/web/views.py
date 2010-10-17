 #!/usr/local/bin/python
 # -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponseForbidden
from techism2.models import Event, Location, StaticPage
from techism2.web.forms import EventForm
from datetime import datetime, timedelta
from techism2 import service, utils
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth import logout as django_logout


def index(request):
    event_list = service.get_event_query_set().order_by('date_time_begin')
    tags = service.get_tags()
    page = __get_paginator_page(request, event_list)
    return render_to_response('events/index.html', {'event_list': page, 'tags': tags}, context_instance=RequestContext(request))

def archive(request):
    event_list = service.get_archived_event_query_set().order_by('-date_time_begin')
    tags = service.get_tags()
    page = __get_paginator_page(request, event_list)
    return render_to_response('events/index.html', {'event_list': page, 'tags': tags}, context_instance=RequestContext(request))

def tag(request, tag_name):
    event_list = service.get_event_query_set().filter(tags=tag_name).order_by('date_time_begin')
    tags = service.get_tags()
    page = __get_paginator_page(request, event_list)
    return render_to_response('events/index.html', {'event_list': page, 'tags': tags, 'tag_name': tag_name}, context_instance=RequestContext(request))

def static_impressum(request):
    return __render_static_page(request, 'static.impressum')

def __render_static_page(request, name):
    page, crated = StaticPage.objects.get_or_create(name=name, defaults={'content': u'<section id="content">Bitte Inhalt einf\u00FCgen.</section>'})
    return render_to_response('events/static.html', {'content': page.content}, context_instance=RequestContext(request))

def create(request):
    button_label = u'Event hinzuf\u00FCgen'
    
    if request.method == 'POST':
        return __save_event(request, button_label)
    
    return render_to_response(
        'events/event.html',
        {
            'form': EventForm(),
            'button_label': button_label
        },
        context_instance=RequestContext(request))

def edit(request, event_id):
    button_label = u'Event \u00E4ndern'
    
    event = Event.objects.get(id=event_id)
    if event.user != request.user and request.user.is_superuser == False:
        return HttpResponseForbidden()
    
    if request.method == 'POST':
        return __save_event(request, button_label, event)
    
    form = __to_event_form(event)
    return render_to_response(
        'events/event.html',
        {
            'form': form,
            'button_label': button_label
        },
        context_instance=RequestContext(request))

def show(request, event_id):
    tags = service.get_tags()
    event = Event.objects.get(id=event_id)
    return render_to_response(
        'events/show.html',
        {
            'event': event,
            'tags': tags
        },
        context_instance=RequestContext(request))

def logout(request):
    django_logout(request)
    return HttpResponseRedirect('/')

def __save_event(request, button_label, old_event=None):
    form = EventForm(request.POST) 
    if form.is_valid(): 
        event= __create_or_update_event_with_location(form, request.user, old_event)
        return HttpResponseRedirect('/events/')
    else:
        return render_to_response(
            'events/event.html',
            {
                'form': form, 
                'error': form.errors,
                'button_label': button_label
            },
            context_instance=RequestContext(request))

def __create_or_update_event_with_location (form, user, event):
    "Creates or updates an Event from the submitted EventForm. If the given Event is None a new Event is created."
    if event == None:
        event = Event()
    
    event.title=form.cleaned_data['title']
    event.set_date_time_begin_cet(form.cleaned_data['date_time_begin'])
    event.set_date_time_end_cet(form.cleaned_data['date_time_end'])
    event.url=form.cleaned_data['url']
    event.description=form.cleaned_data['description']
    event.location=form.cleaned_data['location']
    event.tags=form.cleaned_data['tags']
    
    if event.location == None:
        location = __create_location(form)
        event.location=location
    
    # Only when a new event is created
    if event.id == None:
        # auto-publish for staff users
        event.published = user.is_staff
        # link event to user
        if user.is_authenticated():
            event.user=user
    
    # Compute and store the archived flag
    event.update_archived_flag()
    
    event.save()
    
    return event

def __create_location (form):
    "Creates a Location from the submitted EventForm"
    location = Location()
    location.name=form.cleaned_data['location_name']
    location.street=form.cleaned_data['location_street']
    location.city=form.cleaned_data['location_city']
    if location.name and location.street and location.city:
        location.save()
        return location
    else:
        return None

def __to_event_form (event):
    "Converts an Event to an EventForm"
    data = {'title': event.title,
            'date_time_begin': event.get_date_time_begin_cet(),
            'date_time_begin_0': event.get_date_time_begin_cet(),
            'date_time_begin_1': event.get_date_time_begin_cet(),
            'date_time_end': event.get_date_time_end_cet(),
            'date_time_end_0': event.get_date_time_end_cet(),
            'date_time_end_1': event.get_date_time_end_cet(),
            'url': event.url,
            'description': event.description,
            'location': event.location.id if event.location else None,
            'tags': event.tags,
            #'location_name': event.location.name,
            #'location_street': event.location.street,
            #'location_city': event.location.city
            }
    form = EventForm(data)
    return form;

def __get_paginator_page(request, event_list):
    try:
        num = int(request.GET.get('page', '1'))
    except ValueError:
        num = 1
    
    paginator = Paginator(event_list, 7);
    try:
        page = paginator.page(num)
    except (EmptyPage, InvalidPage):
        page = paginator.page(paginator.num_pages)
    
    return page

