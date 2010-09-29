from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from techism2.events.models import Event
from techism2.events.forms import EventForm
from datetime import datetime
from django.contrib.auth.decorators import login_required

def get_tags():
    # TODO: cache, use django cache which uses GAE memcache
    dict_list = Event.objects.values('tags')
    tags = dict()    
    for dictionary in dict_list:
        for tag_list in dictionary.itervalues():
            if tag_list:
                for tag in tag_list:
                    if tag not in tags:
                        tags[tag] = 0
                    tags[tag] += 1
    return tags
    