from techism2.models import Event
from datetime import datetime


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

