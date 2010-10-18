 #!/usr/local/bin/python
 # -*- coding: utf-8 -*-
from techism2.models import Event
from datetime import datetime
from django.core.cache import cache

tags_cache_key = "tags"


def get_event_query_set():
    "Gets a base query set with all non-archived and published events"
    return __get_base_event_query_set().filter(archived__exact=False)

def get_archived_event_query_set():
    "Gets a base query set with all archived and published events"
    return __get_base_event_query_set().filter(archived__exact=True)

def __get_base_event_query_set():
    return Event.objects.filter(published__exact=True)

def get_tags():
    # Note: no synchronization, propably not possible on GAE
    tags = cache.get(tags_cache_key)
    
    if tags:
        return tags
    else:
        tags = update_tags_cache()
        return tags

def update_tags_cache():
    tags = __fetch_tags()
    cache.set(tags_cache_key, tags, 1800) # expire after 30 min
    return tags

def __fetch_tags():
    dict_list = get_event_query_set().values('tags')
    tags = dict()    
    for dictionary in dict_list:
        for tag_list in dictionary.itervalues():
            if tag_list:
                for tag in tag_list:
                    if tag not in tags:
                        tags[tag] = 0
                    tags[tag] += 1
    return tags

