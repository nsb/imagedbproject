from django.db.models import signals

from photologue import models as photologue_models
from photologue.models import PhotoSize

def init_photologue(*args, **kwargs):
    try:
        admin_thumbnail = PhotoSize.objects.get(name='admin_thumbnail')
    except PhotoSize.DoesNotExist:
        admin_thumbnail = \
            PhotoSize.objects.create(name='admin_thumbnail',
                                     width=100,
                                     height=75,
                                     crop=True,
                                     pre_cache=True)

    try:
        thumbnail = PhotoSize.objects.get(name='thumbnail')
    except PhotoSize.DoesNotExist:
        thumbnail = PhotoSize.objects.create(name='thumbnail', width=100, height=75)

    try:
        display = PhotoSize.objects.get(name='display')
    except PhotoSize.DoesNotExist:
        display = PhotoSize.objects.create(name='display', width=400, increment_count=True)

signals.post_syncdb.connect(init_photologue, sender=photologue_models)