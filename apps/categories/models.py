from django.db import models
from django.utils.translation import ugettext_lazy as _

class Category(models.Model):
    name = models.CharField(_('name'), max_length=255)

    class Meta:
        abstract = True
        ordering = ['name']

    def __unicode__(self):
        return self.name

class Area(Category):
    class Meta:
        verbose_name = _("Geographical area")
        verbose_name_plural = _("Geographical areas")

class Motif(Category):
    class Meta:
        verbose_name = _("Image motif")
        verbose_name_plural = _("Image motifs")

class TimeOfDay(Category):
    class Meta:
        verbose_name = _("Time of day")
        verbose_name_plural = _("Times of day")
