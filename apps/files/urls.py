# Copyright 2008 - 2009, Niels Sandholt Busch <niels.busch@gmail.com>. All rights reserved.

from django.conf.urls.defaults import *

urlpatterns = patterns('files.views',

    (r'^$', 'list', {}, 'list'),
    (r'^photos/page(?P<page>[0-9]+)/$', 'images', {}, 'images'),
    (r'^(?P<image_id>\d+)/$', 'image_detail', {}, 'image-detail'),
    (r'^(?P<image_id>\d+)/(?P<size>(small|medium|large|original))/$', 'send_file', {}, 'image-download'),
    (r'^graphics/page(?P<page>[0-9]+)/$', 'eps', {}, 'eps'),

)
