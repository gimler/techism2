 #!/usr/local/bin/python
 # -*- coding: utf-8 -*-
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from techism2.models import Event
from techism2 import service

class UpcommingEventsAtomFeed(Feed):
    title = "Techism - IT-Events in München"
    link = "/events/"
    description = "Upcomming IT-Events in München"
    feed_type = Atom1Feed

    def items(self):
        return service.get_event_query_set().order_by('date_time_begin')

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description
    
    def item_link(self, item):
        return "/events/" + str(item.id)
    

class UpcommingEventsRssFeed(Feed):
    title = "Techism - IT-Events in München"
    link = "/events/"
    description = "Upcomming IT-Events in München"

    def items(self):
        return service.get_event_query_set().order_by('date_time_begin')

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description
    
    def item_link(self, item):
        return "/events/" + str(item.id)

