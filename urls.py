from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from techism2.rss.feeds import UpcommingEventsRssFeed, UpcommingEventsAtomFeed

admin.autodiscover()

urlpatterns = patterns('',
    # web
    (r'^$', 'techism2.web.views.index'),
    (r'^events/$', 'techism2.web.views.index'),
    url(r'^events/(?P<event_id>\d+)/$', 'techism2.web.views.show', name='event-show'),
    (r'^events/edit/(?P<event_id>\d+)/$', 'techism2.web.views.edit'),
    (r'^events/create/$', 'techism2.web.views.create'),
    (r'^events/archive/$', 'techism2.web.views.archive'),
    (r'^events/tags/(?P<tag_name>.+)/$', 'techism2.web.views.tag'),
    
    # static pages
    (r'^impressum/$', 'techism2.web.views.static_impressum'),
    (r'^about/$', 'techism2.web.views.static_about'),
    
    # iCal
    (r'^feed.ics$', 'techism2.ical.views.ical'),
    
    # Atom
    (r'^feeds/atom/upcomming_events$', UpcommingEventsAtomFeed()),
    
    #RSS
    (r'^feeds/rss/upcomming_events$', UpcommingEventsRssFeed()),
    
    # admin
    (r'^admin/', include(admin.site.urls)),
    
    # login/logout
    (r'^accounts/', include('django_openid_auth.urls')),
    (r'^accounts/logout/$', 'techism2.web.views.logout'),
    url(r'^accounts/google_login/$', 'gaeauth.views.login', name='google_login'),
    url(r'^accounts/google_logout/$', 'gaeauth.views.logout', name='google_logout'),
    url(r'^accounts/google_authenticate/$', 'gaeauth.views.authenticate', name='google_authenticate'),
    
    # cron jobs
    (r'^cron/update_archived_flag', 'techism2.cron.views.update_archived_flag'),
    (r'^cron/update_tags_cache', 'techism2.cron.views.update_tags_cache'),
    

)
