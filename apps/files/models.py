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
    area = models.ForeignKey(Area, null=True, blank=True)
    motif = models.ForeignKey(Motif, null=True, blank=True)
    time_of_day = models.ForeignKey(TimeOfDay, null=True, blank=True)

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

        categories = {'area':self.area, 'motif':self.motif, 'time_of_day':self.time_of_day}
        ids = [str(categories[category].id) if categories[category] else '0' for category in categories]
        new_id = ''.join(ids)
        num_objects = Image.objects.filter(**categories).count()
        index = 1
        try:
            while(True):
                new_title = new_id + str(num_objects + index)
                Image.objects.get(title=new_title)
                index += 1
        except Image.DoesNotExist:
            self.title = new_title

        super(Image, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('image-detail', args=[self.id])
