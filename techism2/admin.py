#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from techism2.models import Event, Location, StaticPage
from django.contrib import admin

class EventAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_filter = ['published', 'archived', 'location']
    list_display = ['title', 'date_time_begin', 'date_time_end', 'location', 'tags', 'archived', 'published']
    list_editable = ['published']

class LocationAdmin(admin.ModelAdmin):
    search_fields = ['name', 'street', 'city']
    list_display = ['name', 'street', 'city']

class StaticPageAdmin(admin.ModelAdmin):
    list_display = ['name', 'content']

admin.site.register(Event, EventAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(StaticPage, StaticPageAdmin)
