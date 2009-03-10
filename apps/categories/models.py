# Copyright 2008 - 2009, Niels Sandholt Busch <niels.busch@gmail.com>. All rights reserved.

from django.db import models
from django.utils.translation import ugettext_lazy as _

class Category(models.Model):
    name = models.CharField(_('name'), max_length=255)

    class Meta:
        abstract = True
        ordering = ['name']

    def __unicode__(self):
        return u'%s' % self.name

class Location(Category):
    class Meta:
        verbose_name = _("Location")
        verbose_name_plural = _("Locations")
        ordering = ['name']

class Field(Category):
    class Meta:
        verbose_name = _("Field")
        verbose_name_plural = _("Fields")
        ordering = ['name']

class Installation(Category):
    class Meta:
        verbose_name = _("Installation & Vessel")
        verbose_name_plural = _("Installations & Vessels")
        ordering = ['name']

class People(Category):
    class Meta:
        verbose_name = _("Person")
        verbose_name_plural = _("People")
        ordering = ['name']

class HSE(Category):
    class Meta:
        verbose_name = _("HSE")
        verbose_name_plural = _("HSE")
        ordering = ['name']

class Event(Category):
    class Meta:
        verbose_name = _("Event")
        verbose_name_plural = _("Events")
        ordering = ['name']

class Graphics(Category):
    class Meta:
        verbose_name = _("Graphics")
        verbose_name_plural = _("Graphics")
        ordering = ['name']

class Communications(Category):
    class Meta:
        verbose_name = _("Communications")
        verbose_name_plural = _("Communications")
        ordering = ['name']

class Archive(Category):
    class Meta:
        verbose_name = _("Archive")
        verbose_name_plural = _("Archives")
        ordering = ['name']
