from datetime import datetime

from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify

from photologue.models import ImageModel

from categories.models import Area, Motif, TimeOfDay

class Image(ImageModel):
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

    def save(self, *args, **kwargs):

        categories = (self.areas, self.motifs, self.times_of_day)

        self.title = \
            '.'.join([''.join([str(val.id) for val in category.all()]) if category.count() > 0 else '0' for category in categories])

        super(Image, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('image-detail', args=[self.id])
