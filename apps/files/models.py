# -*- coding: utf-8 -*-
# Copyright 2008 - 2009, Niels Sandholt Busch <niels.busch@gmail.com>. All rights reserved.

import os
from datetime import datetime
import subprocess
import tempfile

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
from django.conf import settings

from photologue.models import ImageModel, PhotoSizeCache

from categories.models import Location, Installation, People, HSE, Graphics, Communications, Archive, Year, Logo
from rounded_corners import round_image

class Image(ImageModel):
    title = models.CharField(_('title'), max_length=100, unique=True)
    caption = models.TextField(_('image text'), blank=True)
    notes = models.TextField(_('admin comments'), blank=True, null=True)
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
        verbose_name=_('Fields and Installations'))
    people = models.ManyToManyField(
        People,
        null=True,
        blank=True,
        verbose_name=_('People'))
    hse = models.ManyToManyField(
        HSE,
        null=True,
        blank=True,
        verbose_name=_('HSE'))
    graphics = models.ManyToManyField(
        Graphics,
        null=True,
        blank=True,
        verbose_name=_('Graphics'))
    communications = models.ManyToManyField(
        Communications,
        null=True,
        blank=True,
        verbose_name=_('Communications'))
    archives = models.ManyToManyField(
        Archive,
        null=True,
        blank=True,
        verbose_name=_('archives'))
    years = models.ManyToManyField(
        Year,
        null=True,
        blank=True,
        verbose_name=_('years'))

    dont_convert = ['medium', 'large']

    class Meta:
        ordering = ['-date_added']
        get_latest_by = 'date_added'
        verbose_name = _("image")
        verbose_name_plural = _("images")

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.__unicode__()

    def _get_filename_for_size(self, size):
        size = getattr(size, 'name', size)
        base, ext = os.path.splitext(self.image_filename())
        if not size in self.dont_convert:
            # rename to jpg, to ensure webserver sends correct content type
            ext = '.jpg'
        return ''.join([base, '_', size, ext])

    def create_size(self, photosize):
        if self.size_exists(photosize):
            return
        if not os.path.isdir(self.cache_path()):
            os.makedirs(self.cache_path())

        should_convert = lambda s : s.name not in self.dont_convert

        # some images may have CMYK color encoding, so convert to RGB
        # we use tifficc from littlecms utils because pil color space conversion
        # does not give pretty results

        try:
            # get the image format
            im = PILImage.open(self.image.path)
            format = im.format

            # convert to rgb
            retcode = -1
            if should_convert(photosize) and format == 'TIFF':
                input_profile = '%s/iccprofiles/CoatedFOGRA27.icc' % settings.PROJECT_ROOT
                output_profile = '%s/iccprofiles/AdobeRGB1998.icc' % settings.PROJECT_ROOT
                outputfile = tempfile.NamedTemporaryFile()

                retcode = subprocess.call(
                    ['tifficc', "-i", input_profile, "-o", output_profile, self.image.path, outputfile.name])
            im = PILImage.open(outputfile.name if retcode == 0 else self.image.path)

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
        # round corners on thumbnails
        if photosize.name == 'thumbnail':
            im = round_image(im, {}, 10)

        # Save file
        im_filename = getattr(self, "get_%s_filename" % photosize.name)()
        try:
            if im.format != 'JPEG' and should_convert(photosize):

                # save as jpeg
                base, ext = os.path.splitext(im_filename)
                im_filename = ''.join([base, '.jpg'])

                im.save(im_filename, 'JPEG', quality=int(photosize.quality), optimize=True)
                return
            else:
                im.save(im_filename)

        except IOError, e:
            if os.path.isfile(im_filename):
                os.unlink(im_filename)
            raise e

    def size_exists(self, photosize):
        """ encode with utf8 to support unicode filenames"""
        func = getattr(self, "get_%s_filename" % photosize.name, None)
        if func is not None:
            if os.path.isfile(func().encode('utf8')):
                return True
        return False

    def get_original_size(self):
        return PILImage.open(self.image.path).size

    def get_original_filename(self):
        return self.image.path

    def get_file_size(self, size):
        im_filename = getattr(self, "get_%s_filename" % size)()
        return  os.path.getsize(im_filename)

    def get_small_file_size(self):
        return self.get_file_size('small')

    def get_medium_file_size(self):
        return self.get_file_size('medium')

    def get_large_file_size(self):
        return self.get_file_size('large')

    def get_original_file_size(self):
        return self.get_file_size('original')
       
    def get_absolute_url(self):
        return reverse('image-detail', args=[self.id])

    def categories(self):
        locations = ''.join(['%s; ' % location.name for location in self.locations.all()])
        installations = ' '.join(['%s; ' % installation.name for installation in self.installations.all()])
        people = ''.join(['%s; ' % people.name for people in self.people.all()])
        hse = ''.join(['%s; ' % hse.name for hse in self.hse.all()])
        graphics = ''.join(['%s; ' % graphics.name for graphics in self.graphics.all()])
        communications = ''.join(['%s; ' % communications.name for communications in self.communications.all()])
        archives = ''.join(['%s; ' % archive.name for archive in self.archives.all()])
        years = ''.join(['%s; ' % year.name for year in self.years.all()])

        return ''.join([locations, installations, people, hse, graphics, communications, archives, years])

class EPS(models.Model):
    cmyk = models.FileField(upload_to='eps_cmyk', verbose_name='CMYK', null=True, blank=True)
    pantone = models.FileField(upload_to='eps_pantone', null=True, blank=True)
    thumbnail = models.ImageField(upload_to='eps_thumbnails')
    title = models.CharField(_('title'), max_length=100, unique=True)
    caption = models.TextField(_('caption'), blank=True)
    date_added = models.DateTimeField(_('date added'), default=datetime.now, editable=False)
    is_public = models.BooleanField(
        _('is public'),
        default=True,
        help_text=_('Public photographs will be displayed in the default views.'))
    logos = models.ManyToManyField(
        Logo,
        null=True,
        blank=True,
        verbose_name=_('Logos'))

    class Meta:
        ordering = ['-date_added']
        get_latest_by = 'date_added'
        verbose_name = _("EPS")
        verbose_name_plural = _("EPS")

    def save(self, force_insert=False, force_update=False):
        super(EPS, self).save(force_insert, force_update)

        # resize thumbnail
        im = PILImage.open(os.path.join(settings.MEDIA_ROOT, self.thumbnail.name))
        #im = im.resize((100, 100))
        im = self.resize_thumbnail(im)
        im = round_image(im, {}, 10)
        base, ext = os.path.splitext(self.thumbnail.name)
        im.save(os.path.join(settings.MEDIA_ROOT, '%s_thumbnail%s' % (base, ext)))

    def thumbnail_url(self):
        base, ext = os.path.splitext(self.thumbnail.name)
        return os.path.join(settings.MEDIA_URL, '%s_thumbnail%s' % (base, ext)) 

    def admin_thumbnail(self):
        return u'<a href="%s"><img src="%s"></a>' % \
                    (self.thumbnail.url, self.thumbnail_url())
    admin_thumbnail.short_description = _('Thumbnail')
    admin_thumbnail.allow_tags = True

    def categories(self):
        logos = ''.join(['%s; ' % logo.name for logo in self.logos.all()])

        return ''.join([logos])

    def resize_thumbnail(self, im):
        cur_width, cur_height = im.size
        new_width, new_height = (350, 350)
        if not new_width == 0 and not new_height == 0:
            ratio = min(float(new_width)/cur_width,
                        float(new_height)/cur_height)
        else:
            if new_width == 0:
                ratio = float(new_height)/cur_height
            else:
                ratio = float(new_width)/cur_width
        new_dimensions = (int(round(cur_width*ratio)),
                          int(round(cur_height*ratio)))
        if new_dimensions[0] > cur_width or \
            new_dimensions[1] > cur_height:
            return im
        im = im.resize(new_dimensions, PILImage.ANTIALIAS)
        return im
