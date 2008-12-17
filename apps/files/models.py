import os
from datetime import datetime

try:
    import Image
except ImportError:
    try:
        from PIL import Image
    except ImportError:
        raise ImportError('Imagedb was unable to import the Python Imaging Library. Please confirm it`s installed and available on your current Python path.')

from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify

from photologue.models import ImageModel

from categories.models import Area, Motif, TimeOfDay

class MyPhoto(ImageModel):
    title = models.CharField(_('title'), max_length=100, unique=True)
    caption = models.TextField(_('caption'), blank=True)
    date_added = models.DateTimeField(_('date added'), default=datetime.now, editable=False)
    is_public = models.BooleanField(_('is public'),
                                    default=True,
                                    help_text=_('Public photographs will be displayed in the default views.'))
    areas = models.ManyToManyField(Area,
                                   null=True,
                                   blank=True,
                                   verbose_name=_('areas'))
    motifs = models.ManyToManyField(Motif,
                                    null=True,
                                    blank=True,
                                    verbose_name=_('motifs'))
    times_of_day = models.ManyToManyField(TimeOfDay,
                                          null=True,
                                          blank=True,
                                          verbose_name=_('times of day'))

    class Meta:
        ordering = ['-date_added']
        get_latest_by = 'date_added'
        verbose_name = _("photo")
        verbose_name_plural = _("Photos")

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.__unicode__()


    def create_size(self, photosize):
        if self.size_exists(photosize):
            return
        if not os.path.isdir(self.cache_path()):
            os.makedirs(self.cache_path())
        try:
            im = Image.open(self.image.path)
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
        im_filename = getattr(self, "get_%s_filename" % photosize.name)()
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


    def save(self, *args, **kwargs):

        #categories = (self.areas, self.motifs, self.times_of_day)

        #self.title = \
            #'.'.join([''.join([str(val.id) for val in category.all()]) if category.count() else '0' for category in categories])

        self.title = str(datetime.now())
        super(MyPhoto, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('image-detail', args=[self.id])
