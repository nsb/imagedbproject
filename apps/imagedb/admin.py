from django.contrib import admin
from models import Area, Image

class ImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_taken', 'date_added', 'is_public', 'tags', 'view_count', 'admin_thumbnail')
    list_filter = ['date_added', 'is_public']
    list_per_page = 10
    prepopulated_fields = {'title_slug': ('title',)}

admin.site.register(Image, ImageAdmin)

class AreaAdmin(admin.ModelAdmin):
    pass
admin.site.register(Area, AreaAdmin)
