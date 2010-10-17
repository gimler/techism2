from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # web
    (r'^$', 'techism2.web.views.index'),
    (r'^events/$', 'techism2.web.views.index'),
    (r'^events/edit/(?P<event_id>\d+)/$', 'techism2.web.views.edit'),
    (r'^events/create/$', 'techism2.web.views.create'),
    (r'^events/archive/$', 'techism2.web.views.archive'),
    (r'^events/tags/(?P<tag_name>.+)/$', 'techism2.web.views.tag'),
    
    # static pages
    (r'^impressum/$', 'techism2.web.views.static_impressum'),
    
    # iCal
    (r'^feed.ics$', 'techism2.ical.views.ical'),
    
    # admin
    (r'^admin/', include(admin.site.urls)),
    
    # login/logout
    (r'^accounts/', include('django_openid_auth.urls')),
    (r'^accounts/logout/$', 'techism2.web.views.logout'),
    url(r'^accounts/google_login/$', 'auth_helpers.views.login', name='google_login'),
    url(r'^accounts/google_logout/$', 'auth_helpers.views.logout', name='google_logout'),
    url(r'^accounts/google_authenticate/$', 'auth_helpers.views.authenticate', name='google_authenticate'),
    
    # cron jobs
    (r'^cron/update_archived_flag', 'techism2.cron.views.update_archived_flag'),
    (r'^cron/update_tags_cache', 'techism2.cron.views.update_tags_cache'),
    

)
