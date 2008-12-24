import os
from datetime import datetime

try:
    import Image as PILImage
except ImportError:
    try:
        from PIL import Image as PILImage
    except ImportError:
        raise ImportError('Imagedb was unable to import the Python Imaging Library. \
            Please confirm it`s installed and available on your current Python path.')

from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.db import models
from django.core.files.storage import FileSystemStorage
from django.conf import settings

from photologue.models import ImageModel, get_storage_path

from categories.models import Location, Installation, People, HSE, Event, Graphics, Communications

class Image(ImageModel):
    title = models.CharField(_('title'), max_length=100, unique=True)
    caption = models.TextField(_('caption'), blank=True)
    date_added = models.DateTimeField(_('date added'), default=datetime.now, editable=False)
    is_public = models.BooleanField(
        _('is public'),
        default=True,
        help_text=_('Public photographs will be displayed in the default views.'))
    locations = models.ManyToManyField(
        Location,
        null=True,
        blank=True,
        verbose_name=_('Locations'))
    installations = models.ManyToManyField(
        Installation,
        null=True,
        blank=True,
        verbose_name=_('Installations & Vessels'))
    people = models.ManyToManyField(
        People,
        null=True,
        blank=True,
        verbose_name=_('times of day'))
    hse = models.ManyToManyField(
        HSE,
        null=True,
        blank=True,
        verbose_name=_('HSE'))
    events = models.ManyToManyField(
        Event,
        null=True,
        blank=True,
        verbose_name=_('Events'))
    graphics = models.ManyToManyField(
        Graphics,
        null=True,
        blank=True,
        verbose_name=_('Graphics'))
    communications = models.ManyToManyField(
        Communications,
        null=True,
        blank=True,
        verbose_name=_('areas'))

    class Meta:
        ordering = ['-date_added']
        get_latest_by = 'date_added'
        verbose_name = _("photo")
        verbose_name_plural = _("Photos")

    def __init__(self, *args, **kwargs):
        super(Image, self).__init__(*args, **kwargs)
        fs = FileSystemStorage(location='/home/niels/imagedb_upload')
        self.image.storage = fs


    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.__unicode__()

    #def cache_path(self, size):
        #if size in ('admin_thumbnail', 'thumbnail'):
            #return os.path.join(settings.MEDIA_ROOT, 'photologue', 'photos', 'cache')
        #else:
            #return os.path.join(os.path.dirname(self.image.path), "cache")
        ##return os.path.join('/home/niels/programming/imagedb/static/photologue/photos', "cache")

    def get_imagedb_filename(self, size):
        if size in ('admin_thumbnail', 'thumbnail'):
            return os.path.join(settings.MEDIA_ROOT, 'photologue', 'photos', 'cache', self._get_filename_for_size(size))
        else:
            return getattr(self, "get_%s_filename" % size)()

    def create_size(self, photosize):
        if self.size_exists(photosize):
            return
        if not os.path.isdir(self.cache_path()):
            os.makedirs(self.cache_path())
        try:
            im = PILImage.open(self.image.path)
        except IOError:
            return
        # Apply effect if found
        if self.effect is not None:
            im = self.effect.pre_process(im)
        elif photosize.effect is not None:
            im = photosize.effect.pre_process(im)
        # Resize/crop image
        if im.size != photosize.size and photosize.size != (0, 0):
            im = self.resize_image(im, photosize)
        # Apply watermark if found
        if photosize.watermark is not None:
            im = photosize.watermark.post_process(im)
        # Apply effect if found
        if self.effect is not None:
            im = self.effect.post_process(im)
        elif photosize.effect is not None:
            im = photosize.effect.post_process(im)
        # Save file
        im_filename = self.get_imagedb_filename(photosize.name)
        try:
            if im.format != 'JPEG':
                try:
                    if photosize.name not in ('small', 'medium', 'large'):
                        im.save(im_filename, 'JPEG', quality=int(photosize.quality), optimize=True)
                    else:
                        im.save(im_filename)
                    return
                except KeyError:
                    pass
            im.save(im_filename, 'JPEG', quality=int(photosize.quality), optimize=True)
        except IOError, e:
            if os.path.isfile(im_filename):
                os.unlink(im_filename)
            raise e

    def get_original_size(self):
        return PILImage.open(self.image.path).size

    def get_absolute_url(self):
        return reverse('image-detail', args=[self.id])
