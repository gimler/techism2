from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^resources/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_DOC_ROOT}),
    (r'^events/$', 'techism2.events.views.index'),
    (r'^events/(?P<event_id>\d+)/$', 'techism2.events.views.detail'),
    (r'^events/(?P<event_id>\d+)/results/$', 'techism2.events.views.results'),
    (r'^admin/', include(admin.site.urls)),
)
