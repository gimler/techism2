from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'techism2.events.views.index'),
    (r'^events/$', 'techism2.events.views.index'),
    (r'^events/(?P<event_id>\d+)/$', 'techism2.events.views.detail'),
    (r'^events/create/$', 'techism2.events.views.create'),
    (r'^events/archive/$', 'techism2.events.views.archive'),
    (r'^events/impressum/$', 'techism2.events.views.impressum'),
    (r'^events/tags/(?P<tag_name>.+)/$', 'techism2.events.views.tag'),
    
    (r'^admin/', include(admin.site.urls)),
    
    (r'^accounts/', include('django_openid_auth.urls')),
    (r'^accounts/logout/$', 'techism2.events.views.logout'),

)
