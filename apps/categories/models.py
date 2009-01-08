from django.db import models
from django.utils.translation import ugettext_lazy as _

class Category(models.Model):
    name = models.CharField(_('name'), max_length=255)

    class Meta:
        abstract = True
        ordering = ['name']

    def __unicode__(self):
        return u'%s (%d)' % (self.name, self.image_set.count())

class Location(Category):
    class Meta:
        verbose_name = _("Location")
        verbose_name_plural = _("Locations")

class Installation(Category):
    class Meta:
        verbose_name = _("Installation & Vessel")
        verbose_name_plural = _("Installations & Vessels")

class People(Category):
    class Meta:
        verbose_name = _("Person")
        verbose_name_plural = _("People")

class HSE(Category):
    class Meta:
        verbose_name = _("HSE")
        verbose_name_plural = _("HSE")

class Event(Category):
    class Meta:
        verbose_name = _("Event")
        verbose_name_plural = _("Events")

class Graphics(Category):
    class Meta:
        verbose_name = _("Graphics")
        verbose_name_plural = _("Graphics")

class Communications(Category):
    class Meta:
        verbose_name = _("Communications")
        verbose_name_plural = _("Communications")
