# -*- coding: utf-8 -*-
# Copyright 2008 - 2009, Niels Sandholt Busch <niels.busch@gmail.com>. All rights reserved.

from django.conf.urls.defaults import *

urlpatterns = patterns('files.views',

    (r'^$', 'image_front', {}, 'image_front'),
    (r'^images/page(?P<page>[0-9]+)/$', 'images', {}, 'images'),
    (r'^images/(?P<image_id>\d+)/$', 'image_detail', {}, 'image-detail'),
    (r'^images/(?P<image_id>\d+)/(?P<size>(small|medium|large|original))/$', 'send_image', {}, 'image-download'),
    (r'^logos/$', 'eps_front', {}, 'eps_front'),
    (r'^logos/page(?P<page>[0-9]+)/$', 'eps', {}, 'eps'),
    (r'^logos/(?P<eps_id>\d+)/$', 'eps_detail', {}, 'eps-detail'),
    (r'^logos/(?P<eps_id>\d+)/original/$', 'send_eps', {}, 'eps-download'),

)
