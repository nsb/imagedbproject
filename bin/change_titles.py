# -*- coding: utf-8 -*-

import sys, os

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../apps')
sys.path.append("/home/ciboe/lib")
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from files.models import Image

for image in Image.objects.all():

    locations = ''.join([str(val.id) for val in image.locations.all()]) or '0'
    installations = ''.join([str(val.id) for val in image.installations.all()]) or '0'
    people = ''.join([str(val.id) for val in image.people.all()]) or '0'
    communications = ''.join([str(val.id) for val in image.communications.all()]) or '0'
    hse = ''.join([str(val.id) for val in image.hse.all()]) or '0'
    graphics = ''.join([str(val.id) for val in image.graphics.all()]) or '0'
    years = ''.join([str(val.id) for val in image.years.all()]) or '0'
    archives = ''.join([str(val.id) for val in image.archives.all()]) or '0'

    title = '.'.join((
        locations,
        installations,
        people,
        communications,
        hse,
        graphics,
        years,
        archives,
    ))

    c = 1
    # check if title exists before saving
    while(True):
        new_title = '%s.%d' % (title, c)
        try:
            im = Image.objects.get(title=new_title)
            c += 1
        except Image.DoesNotExist:
            break

    image.title = new_title
    print new_title
    image.save()
