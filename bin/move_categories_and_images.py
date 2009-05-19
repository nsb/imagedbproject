# -*- coding: utf-8 -*-

import sys, os

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../apps')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from categories.models import Event, Communications
from files.models import Image

for image in Image.objects.all():
    for event in image.events.all():
        communication, created = Communications.objects.get_or_create(name=event.name)
        image.communications.add(communication)
        image.events.remove(event)
