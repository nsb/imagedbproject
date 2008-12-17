from datetime import datetime

from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site

from photologue.models import *

from models import MyPhoto

class MyPhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_taken', 'date_added', 'is_public', 'view_count', 'admin_thumbnail')
    list_filter = ['date_added', 'is_public', 'areas', 'motifs', 'times_of_day',]
    list_per_page = 10
    save_on_top = True
    filter_horizontal = ('areas', 'motifs', 'times_of_day',)
    fieldsets = (
        (None, {
            'fields': ('image',)
        }),
        ('Categories', {
            'fields': ('areas', 'motifs', 'times_of_day',)
        }),
        ('Options', {
            'fields': ('is_public',)
        }),
    )

    def save_model(self, request, obj, form, change):
        """
        Given a model instance save it to the database.
        """

        categories = ('areas', 'motifs', 'times_of_day')

        if form.is_valid():
            obj.title = \
                '.'.join([''.join([str(val.id) for val in form.cleaned_data[category]]) if form.cleaned_data[category] else '0' for category in categories])

        obj.save()

class PhotoSizeAdmin(admin.ModelAdmin):
    list_display = ('name', 'width', 'height', 'crop', 'pre_cache', 'increment_count')
    fieldsets = (
        (None, {
            'fields': ('name', 'width', 'height', 'quality')
        }),
        ('Options', {
            'classes': ('collapse',),
            'fields': ('upscale', 'crop', 'pre_cache', 'increment_count')
        }),
    )

admin.site.unregister(Gallery)
admin.site.unregister(GalleryUpload)
admin.site.unregister(Photo)
admin.site.unregister(PhotoEffect)
admin.site.unregister(PhotoSize)
admin.site.unregister(Watermark)

admin.site.unregister(Group)
admin.site.unregister(Site)

admin.site.register(MyPhoto, MyPhotoAdmin)
admin.site.register(PhotoSize, PhotoSizeAdmin)
