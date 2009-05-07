# -*- coding: utf-8 -*-
# Copyright 2008 - 2009, Niels Sandholt Busch <niels.busch@gmail.com>. All rights reserved.

from django.contrib import admin

from models import Location, Field, Installation, People, HSE, Event, Graphics, Communications, Archive, Year, Logo

admin.site.register(Location)
admin.site.register(Field)
admin.site.register(Installation)
admin.site.register(People)
admin.site.register(HSE)
admin.site.register(Event)
admin.site.register(Graphics)
admin.site.register(Communications)
admin.site.register(Archive)
admin.site.register(Year)
admin.site.register(Logo)
