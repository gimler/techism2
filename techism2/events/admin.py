from techism2.events.models import Event
from django.contrib import admin

class EventAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['title']}),
        ('Event details', {'fields': ['date','url']}),
    ]
    list_filter = ['date']
    search_fields = ['title']
    date_hierarchy = 'date'

admin.site.register(Event)
