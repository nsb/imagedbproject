# Copyright 2008 - 2009, Niels Sandholt Busch <niels.busch@gmail.com>. All rights reserved.

from django.conf.urls.defaults import *

urlpatterns = patterns('files.views',

    (r'^$', 'list', {}, 'image-list'),
    (r'^page(?P<page>[0-9]+)/$', 'list', {}, 'image-list'),
    (r'^filter/page(?P<page>[0-9]+)/$', 'filter', {}, 'image-filter'),
    (r'^(?P<image_id>\d+)/$', 'detail', {}, 'image-detail'),
    (r'^(?P<image_id>\d+)/(?P<size>(small|medium|large|original|eps))/$', 'send_file', {}, 'image-download'),
)
