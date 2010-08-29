# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *


urlpatterns = patterns('',
   url(r'^login/$', 'auth_helpers.views.login', name='google_login'),
   url(r'^logout/$', 'auth_helpers.views.logout', name='google_logout'),
   url(r'^authenticate/$', 'auth_helpers.views.authenticate', name='google_authenticate'),
)
