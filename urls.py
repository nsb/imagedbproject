# Copyright 2008 - 2009, Niels Sandholt Busch <niels.busch@gmail.com>. All rights reserved.

from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib.auth import views as auth_views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^imagedb/', include('imagedb.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/(.*)', admin.site.root),

    url(r'^login/$',
        auth_views.login,
        {'template_name': 'login.html'},
        name='auth_login'),
    url(r'^logout/$',
        auth_views.logout,
        {'template_name': 'logout.html', 'next_page':'/',},
        name='auth_logout'),
    url(r'^password/change/$',
        auth_views.password_change,
        name='auth_password_change'),
    url(r'^password/change/done/$',
        auth_views.password_change_done,
        name='auth_password_change_done'),
    url(r'^password/reset/$',
        auth_views.password_reset,
        name='auth_password_reset'),
    url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        auth_views.password_reset_confirm,
        name='auth_password_reset_confirm'),
    url(r'^password/reset/complete/$',
        auth_views.password_reset_complete,
        name='auth_password_reset_complete'),
    url(r'^password/reset/done/$',
        auth_views.password_reset_done,
        name='auth_password_reset_done'),

    (r'^', include('files.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('', 
        (r'^static/(?P<path>.*)$',
         'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    ) 