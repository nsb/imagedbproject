from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site

from photologue.models import *

from models import Image

class ImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_taken', 'date_added', 'is_public', 'view_count', 'admin_thumbnail')
    list_filter = ['date_added', 'is_public', 'locations', 'installations', 'people', 'hse', 'events', 'graphics', 'communications',]
    list_per_page = 10
    save_on_top = True
    #filter_horizontal = ('locations', 'installations', 'people', 'hse', 'events', 'graphics', 'communications',)
    fieldsets = (
        (None, {
            'fields': ('image',)
        }),
        ('Categories', {
            'fields': ('locations', 'installations', 'people', 'hse', 'events', 'graphics', 'communications',)
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
            (('%s' % key, [value for value in values]) if values else (key, None) \
                for (key, values) in form.cleaned_data.items() if key in categories)

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

admin.site.register(Image, ImageAdmin)
admin.site.register(PhotoSize, PhotoSizeAdmin)
