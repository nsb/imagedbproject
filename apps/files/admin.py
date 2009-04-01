# Copyright 2008 - 2009, Niels Sandholt Busch <niels.busch@gmail.com>. All rights reserved.

from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.sites.models import Site
from django.contrib.auth.admin import UserAdmin

from photologue.models import *

from categories.models import Year
from models import Image

class ImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_taken', 'date_added', 'is_public', 'view_count', 'admin_thumbnail')
    list_filter = ['date_added', 'is_public', 'locations', 'fields', 'installations', 'people', 'hse', 'events', 'graphics', 'communications', 'archives', 'years']
    list_per_page = 10
    save_on_top = True
    #actions = [set_year_factory(year) for year in Year.objects.all()]
    actions = ['set_1985', 'set_1986', 'set_1987', 'set_1988', 'set_1989', 'set_1990', 'set_1991', 'set_1992', 'set_1993', 'set_1994', 'set_1995', 'set_1996', 'set_1997', 'set_1998', 'set_1999', 'set_2000', 'set_2001', 'set_2002', 'set_2003', 'set_2004', 'set_2005', 'set_2006', 'set_2007', 'set_2008', 'set_2009',]
    fieldsets = (
        (None, {
            'fields': ('image',)
        }),
        ('Categories', {
            'fields': ('locations', 'fields', 'installations', 'people', 'hse', 'events', 'graphics', 'communications', 'archives', 'years',)
        }),
        ('Options', {
            'fields': ('is_public',)
        }),
    )

    def set_1985(self, request, queryset):
        for im in queryset:
            im.years.add(Year.objects.get(name='1985'))
        self.message_user(request, "Succesfully added year to %s images." % queryset.count())
    set_1985.short_description = '1985'

    def set_1986(self, request, queryset):
        for im in queryset:
            im.years.add(Year.objects.get(name='1986'))
        self.message_user(request, "Succesfully added year to %s images." % queryset.count())
    set_1986.short_description = '1986'

    def set_1987(self, request, queryset):
        for im in queryset:
            im.years.add(Year.objects.get(name='1987'))
        self.message_user(request, "Succesfully added year to %s images." % queryset.count())
    set_1987.short_description = '1987'

    def set_1988(self, request, queryset):
        for im in queryset:
            im.years.add(Year.objects.get(name='1988'))
        self.message_user(request, "Succesfully added year to %s images." % queryset.count())
    set_1988.short_description = '1988'

    def set_1989(self, request, queryset):
        for im in queryset:
            im.years.add(Year.objects.get(name='1989'))
        self.message_user(request, "Succesfully added year to %s images." % queryset.count())
    set_1989.short_description = '1989'

    def set_1990(self, request, queryset):
        for im in queryset:
            im.years.add(Year.objects.get(name='1990'))
        self.message_user(request, "Succesfully added year to %s images." % queryset.count())
    set_1990.short_description = '1990'

    def set_1991(self, request, queryset):
        for im in queryset:
            im.years.add(Year.objects.get(name='1991'))
        self.message_user(request, "Succesfully added year to %s images." % queryset.count())
    set_1991.short_description = '1991'

    def set_1992(self, request, queryset):
        for im in queryset:
            im.years.add(Year.objects.get(name='1992'))
        self.message_user(request, "Succesfully added year to %s images." % queryset.count())
    set_1992.short_description = '1992'

    def set_1993(self, request, queryset):
        for im in queryset:
            im.years.add(Year.objects.get(name='1993'))
        self.message_user(request, "Succesfully added year to %s images." % queryset.count())
    set_1993.short_description = '1993'

    def set_1994(self, request, queryset):
        for im in queryset:
            im.years.add(Year.objects.get(name='1994'))
        self.message_user(request, "Succesfully added year to %s images." % queryset.count())
    set_1994.short_description = '1994'

    def set_1995(self, request, queryset):
        for im in queryset:
            im.years.add(Year.objects.get(name='1995'))
        self.message_user(request, "Succesfully added year to %s images." % queryset.count())
    set_1995.short_description = '1995'

    def set_1996(self, request, queryset):
        for im in queryset:
            im.years.add(Year.objects.get(name='1996'))
        self.message_user(request, "Succesfully added year to %s images." % queryset.count())
    set_1996.short_description = '1996'

    def set_1997(self, request, queryset):
        for im in queryset:
            im.years.add(Year.objects.get(name='1997'))
        self.message_user(request, "Succesfully added year to %s images." % queryset.count())
    set_1997.short_description = '1997'

    def set_1998(self, request, queryset):
        for im in queryset:
            im.years.add(Year.objects.get(name='1998'))
        self.message_user(request, "Succesfully added year to %s images." % queryset.count())
    set_1998.short_description = '1998'

    def set_1999(self, request, queryset):
        for im in queryset:
            im.years.add(Year.objects.get(name='1999'))
        self.message_user(request, "Succesfully added year to %s images." % queryset.count())
    set_1999.short_description = '1999'

    def set_2000(self, request, queryset):
        for im in queryset:
            im.years.add(Year.objects.get(name='2000'))
        self.message_user(request, "Succesfully added year to %s images." % queryset.count())
    set_2000.short_description = '2000'

    def set_2001(self, request, queryset):
        for im in queryset:
            im.years.add(Year.objects.get(name='2001'))
        self.message_user(request, "Succesfully added year to %s images." % queryset.count())
    set_2001.short_description = '2001'

    def set_2002(self, request, queryset):
        for im in queryset:
            im.years.add(Year.objects.get(name='2002'))
        self.message_user(request, "Succesfully added year to %s images." % queryset.count())
    set_2002.short_description = '2002'

    def set_2003(self, request, queryset):
        for im in queryset:
            im.years.add(Year.objects.get(name='2003'))
        self.message_user(request, "Succesfully added year to %s images." % queryset.count())
    set_2003.short_description = '2003'

    def set_2004(self, request, queryset):
        for im in queryset:
            im.years.add(Year.objects.get(name='2003'))
        self.message_user(request, "Succesfully added year to %s images." % queryset.count())
    set_2004.short_description = '2004'

    def set_2005(self, request, queryset):
        for im in queryset:
            im.years.add(Year.objects.get(name='2005'))
        self.message_user(request, "Succesfully added year to %s images." % queryset.count())
    set_2005.short_description = '2005'

    def set_2006(self, request, queryset):
        for im in queryset:
            im.years.add(Year.objects.get(name='2006'))
        self.message_user(request, "Succesfully added year to %s images." % queryset.count())
    set_2006.short_description = '2006'

    def set_2007(self, request, queryset):
        for im in queryset:
            im.years.add(Year.objects.get(name='2007'))
        self.message_user(request, "Succesfully added year to %s images." % queryset.count())
    set_2007.short_description = '2007'

    def set_2008(self, request, queryset):
        for im in queryset:
            im.years.add(Year.objects.get(name='2008'))
        self.message_user(request, "Succesfully added year to %s images." % queryset.count())
    set_2008.short_description = '2008'

    def set_2009(self, request, queryset):
        for im in queryset:
            im.years.add(Year.objects.get(name='2009'))
        self.message_user(request, "Succesfully added year to %s images." % queryset.count())
    set_2009.short_description = '2009'

    def save_model(self, request, obj, form, change):
        """
        Given a model instance save it to the database.
        """
        categories = self.fieldsets[1][1]['fields']

        if form.is_valid():
            title = \
                '.'.join([''.join([str(val.id) for val in form.cleaned_data[category]]) if form.cleaned_data[category] else '0' for category in categories])

            lookup_args = \
                ((key, values or None) for (key, values) in form.cleaned_data.items() if key in categories)

            if change and not form.has_changed():
                obj.save()
            else:
                qs = Image.objects.all()
                for key, val in lookup_args:
                    if val:
                        for v in val:
                            qs = qs.filter(**{key:v})
                    else:
                        qs = qs.filter(**{key:val})
                c = qs.distinct().count()

                # check if title exists before saving
                while(True):
                    new_title = '%s.%d' % (title, c or 1)
                    try:
                        im = Image.objects.get(title=new_title)
                        c += 1
                    except Image.DoesNotExist:
                        break

                obj.title = new_title
                obj.save()

class PhotoSizeAdmin(admin.ModelAdmin):
    list_display = ('name', 'width', 'height', 'crop', 'pre_cache', 'increment_count')
    fieldsets = (
        (None, {
            'fields': ('width', 'height', 'quality')
        }),
        ('Options', {
            'classes': ('collapse',),
            'fields': ('upscale', 'crop', 'pre_cache', 'increment_count')
        }),
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

class UserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff',)
    list_filter = ['is_staff', 'is_superuser',] 
    fieldsets = (
        (None, {
            'fields': ('username', 'password',)
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email',)
        }),
        ('Permissions', {
            'fields': ('is_staff', 'is_active', 'is_superuser',)
        }),
    )

admin.site.unregister(Gallery)
admin.site.unregister(GalleryUpload)
admin.site.unregister(Photo)
admin.site.unregister(PhotoEffect)
admin.site.unregister(PhotoSize)
admin.site.unregister(Watermark)

admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.unregister(Site)

admin.site.register(User, UserAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(PhotoSize, PhotoSizeAdmin)
