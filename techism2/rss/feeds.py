#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from techism2 import service

 

class UpcommingEventsRssFeed(Feed):
    title = "Techism - IT-Events in München"
    link = "/events/"
    description = "Upcomming IT-Events in München"

    def items(self):
        return service.get_event_query_set().order_by('date_time_begin')

    def item_title(self, item):
        if item.date_time_end is not None:
            dateString = item.date_time_begin.strftime("%d.%m.%Y") + "-" + item.date_time_end.strftime("%d.%m.%Y")
        else:
            dateString = item.date_time_begin.strftime("%d.%m.%Y %H:%M")
        return item.title + " - " + dateString

    def item_description(self, item):
        return item.description
    
    def item_link(self, item):
        return "/events/" + str(item.id)
    

class UpcommingEventsAtomFeed(UpcommingEventsRssFeed):
    feed_type = Atom1Feed


