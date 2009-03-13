# Copyright 2008 - 2009, Niels Sandholt Busch <niels.busch@gmail.com>. All rights reserved.

from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.sites.models import Site
from django.contrib.auth.admin import UserAdmin
from django.core.exceptions import PermissionDenied

from photologue.models import *

from models import Image

class ImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_taken', 'date_added', 'is_public', 'view_count', 'admin_thumbnail')
    list_filter = ['date_added', 'is_public', 'locations', 'fields', 'installations', 'people', 'hse', 'events', 'graphics', 'communications', 'archives',]
    list_per_page = 10
    save_on_top = True
    fieldsets = (
        (None, {
            'fields': ('image',)
        }),
        ('Categories', {
            'fields': ('locations', 'fields', 'installations', 'people', 'hse', 'events', 'graphics', 'communications', 'archives',)
        }),
        ('Options', {
            'fields': ('is_public',)
        }),
    )

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
