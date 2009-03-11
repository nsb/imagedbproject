# Copyright 2008 - 2009, Niels Sandholt Busch <niels.busch@gmail.com>. All rights reserved.

from django.db.models import signals

from photologue import models as photologue_models
from photologue.models import PhotoSize

def init_photologue(*args, **kwargs):

    default_photo_sizes = (
        {'name':'admin_thumbnail', 'width':100, 'height':75, 'crop':True, 'pre_cache':True},
        {'name':'thumbnail', 'width':200, 'height':200, 'crop':True},
        {'name':'display', 'width':800, 'increment_count':True},
        {'name':'small', 'width':400},
        {'name':'medium', 'width':800},
        {'name':'large', 'width':1200},
    )

    for ps in default_photo_sizes:
        try:
            PhotoSize.objects.get(name=ps['name'])
        except PhotoSize.DoesNotExist:
            PhotoSize.objects.create(**ps)

signals.post_syncdb.connect(init_photologue, sender=photologue_models)