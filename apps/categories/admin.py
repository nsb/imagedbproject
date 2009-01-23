# Copyright 2008 - 2009, Niels Sandholt Busch <niels.busch@gmail.com>. All rights reserved.

from django.contrib import admin

from models import Location, Installation, People, HSE, Event, Graphics, Communications

admin.site.register(Location)
admin.site.register(Installation)
admin.site.register(People)
admin.site.register(HSE)
admin.site.register(Event)
admin.site.register(Graphics)
admin.site.register(Communications)

