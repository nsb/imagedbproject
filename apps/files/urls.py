# -*- coding: utf-8 -*-
# Copyright 2008 - 2009, Niels Sandholt Busch <niels.busch@gmail.com>. All rights reserved.

from django.conf.urls.defaults import *

urlpatterns = patterns('files.views',

    (r'^$', 'image_front', {}, 'image_front'),
    (r'^images/page(?P<page>[0-9]+)/$', 'images', {}, 'images'),
    (r'^images/(?P<image_id>\d+)/$', 'image_detail', {}, 'image-detail'),
    (r'^images/(?P<image_id>\d+)/(?P<size>(small|medium|large|original))/$', 'send_image', {}, 'image-download'),
<<<<<<< HEAD:apps/files/urls.py
=======
    (r'^images/downloadfolder/$', 'image_downloadfolder_view', {}, 'image_downloadfolder_view'),
    (r'^images/downloadfolder/update/$', 'image_downloadfolder_update', {}, "image_downloadfolder_update"),
    (r'^images/downloadfolder/download/$', 'image_downloadfolder_download', {}, 'image_downloadfolder_download'),
    (r'^images/downloadfolder/clear/$', 'image_downloadfolder_clear', {}, 'image_downloadfolder_clear'),
    (r'^images/downloadfolder/toggle/$', 'image_downloadfolder_toggle', {}, 'image_downloadfolder_toggle'),
>>>>>>> ff161db9ad24fb5cb5c3706bae393fd97e263f77:apps/files/urls.py
    (r'^logos/$', 'eps_front', {}, 'eps_front'),
    (r'^logos/page(?P<page>[0-9]+)/$', 'eps', {}, 'eps'),
    (r'^logos/(?P<eps_id>\d+)/$', 'eps_detail', {}, 'eps-detail'),
    (r'^logos/(?P<eps_id>\d+)/original/$', 'send_eps', {}, 'eps-download'),
    (r'^logos/(?P<eps_id>\d+)/cmyk/$', 'send_cmyk', {}, 'eps-cmyk-download'),
    (r'^logos/(?P<eps_id>\d+)/pantone/$', 'send_pantone', {}, 'eps-pantone-download'),
)
