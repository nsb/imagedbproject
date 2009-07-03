# -*- coding: utf-8 -*-
# Copyright 2008 - 2009, Niels Sandholt Busch <niels.busch@gmail.com>. All rights reserved.

from django.contrib import admin

from models import Location, Installation, People, HSE, Graphics, Communications, Archive, Year, Logo

class CategoryModelAdmin(admin.ModelAdmin):
    actions = None

admin.site.register(Location, CategoryModelAdmin)
admin.site.register(Installation, CategoryModelAdmin)
admin.site.register(People, CategoryModelAdmin)
admin.site.register(HSE, CategoryModelAdmin)
admin.site.register(Graphics, CategoryModelAdmin)
admin.site.register(Communications, CategoryModelAdmin)
admin.site.register(Archive, CategoryModelAdmin)
admin.site.register(Year, CategoryModelAdmin)
admin.site.register(Logo, CategoryModelAdmin)
