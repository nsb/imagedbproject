from django.conf.urls.defaults import *

urlpatterns = patterns('files.views',

    (r'^$', 'list', {}, 'image-list'),
    (r'^page(?P<page>[0-9]+)/$', 'list', {}, 'image-list'),
    (r'^filter/page(?P<page>[0-9]+)/$', 'filter', {}, 'image-filter'),
    (r'^(?P<image_id>\d+)/$', 'detail', {}, 'image-detail'),
)
