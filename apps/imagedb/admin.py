from django.contrib import admin

from django.contrib.auth.models import Group
from django.contrib.sites.models import Site

from tagging.models import Tag, TaggedItem
from photologue.models import *

from models import Area, Motif, TimeOfDay, Image

class ImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_taken', 'date_added', 'is_public', 'tags', 'view_count', 'admin_thumbnail')
    list_filter = ['date_added', 'is_public', 'area', 'motif', 'time_of_day',]
    list_per_page = 10
    prepopulated_fields = {'title_slug': ('title',)}
    fieldsets = (
        (None, {
            'fields': ('image', 'title', 'title_slug')
        }),
        ('Categories', {
            'fields': ('area', 'motif', 'time_of_day',)
        }),
        ('Options', {
            'classes': ('collapse',),
            'fields': ('is_public', 'tags')
        }),
    )

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

admin.site.unregister(TaggedItem)
admin.site.unregister(Tag)

admin.site.unregister(Group)
admin.site.unregister(Site)

admin.site.register(Image, ImageAdmin)
admin.site.register(Area)
admin.site.register(Motif)
admin.site.register(TimeOfDay)
admin.site.register(PhotoSize, PhotoSizeAdmin)
