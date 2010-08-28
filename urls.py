from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^events/$', 'techism2.events.views.index'),
    (r'^events/(?P<event_id>\d+)/$', 'techism2.events.views.detail'),
    (r'^events/create/$', 'techism2.events.views.create'),
    (r'^admin/', include(admin.site.urls)),
)
