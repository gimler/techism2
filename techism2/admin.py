from techism2.models import Event, Location
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
admin.site.register(Location)