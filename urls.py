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
    
    (r'^admin/', include(admin.site.urls)),
    
    url(r'^accounts/login/$', 'auth_helpers.views.login', name='google_login'),
    url(r'^accounts/logout/$', 'auth_helpers.views.logout', name='google_logout'),
    url(r'^accounts/authenticate/$', 'auth_helpers.views.authenticate', name='google_authenticate'),
    #(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),

)
