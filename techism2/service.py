from techism2.models import Event
from datetime import datetime
from django.core.cache import cache

tags_cache_key = "tags"

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
    dict_list = Event.objects.filter(archived__exact=False).values('tags')
    tags = dict()    
    for dictionary in dict_list:
        for tag_list in dictionary.itervalues():
            if tag_list:
                for tag in tag_list:
                    if tag not in tags:
                        tags[tag] = 0
                    tags[tag] += 1
    return tags

