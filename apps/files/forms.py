# -*- coding: utf-8 -*-
# Copyright 2008 - 2009, Niels Sandholt Busch <niels.busch@gmail.com>. All rights reserved.

from django import forms
from django.forms.forms import BoundField

from categories.models import Location, Field, Installation, People, HSE, Graphics, Communications, Archive, Year, Logo

class Fieldset(object):
    def __init__(self, form, name=None, fields=(), description=None):
        self.form = form
        self.name, self.fields = name, fields
        self.description = description

    def __iter__(self):
        for name in self.fields:
            yield BoundField(self.form, self.form.fields[name], name)

def imagefilterform_factory(request):

    class ImageFilterForm(forms.Form):
        locations = forms.ChoiceField(label='Locations', required=False)
        fields = forms.ChoiceField(label='Fields', required=False)
        installations = forms.ChoiceField(label='Installations & Vessels', required=False)
        people = forms.ChoiceField(label='People', required=False)
        hse = forms.ChoiceField(label='HSE', required=False)
        graphics = forms.ChoiceField(label='Graphics', required=False)
        years = forms.ChoiceField(label='Year', required=False)

        def __init__(self, *args, **kwargs):
            self.fieldsets = []
            super(ImageFilterForm, self).__init__(*args, **kwargs)
        
            _choices = lambda x: [('','')] + ([('all','All')] if x.count() else []) + \
                [(item.name, '%s (%d)' % (item.name, item.image_set.count())) for item in x]

            self.fields['locations'].choices = _choices(Location.objects.all())
            self.fields['fields'].choices = _choices(Field.objects.all())
            self.fields['installations'].choices = _choices(Installation.objects.all())
            self.fields['people'].choices = _choices(People.objects.all())
            self.fields['hse'].choices = _choices(HSE.objects.all())
            self.fields['graphics'].choices = _choices(Graphics.objects.all())
            self.fields['years'].choices = _choices(Year.objects.all())

            if request.user.is_staff:
                self.fields['communications'] = \
                    forms.ChoiceField(label='Communications use only', required=False)
                self.fields['archives'] = \
                    forms.ChoiceField(label='Archive', required=False)

                self.fields['communications'].choices = _choices(Communications.objects.all())
                self.fields['archives'].choices = _choices(Archive.objects.all())

            self.fieldsets.append(
                Fieldset(self, name='', fields=('locations', 'fields', 'installations', 'people', 'years',)))
            self.fieldsets.append(Fieldset(self, name='', fields=('hse', 'graphics', 'communications', 'archives',) if request.user.is_staff else ('hse', 'graphics',)))

    return ImageFilterForm

class EPSFilterForm(forms.Form):
    logos = forms.ChoiceField(label='Logos', required=False)

    def __init__(self, *args, **kwargs):
        self.fieldsets = []
        super(EPSFilterForm, self).__init__(*args, **kwargs)
        
        _choices = lambda x: [('','')] + ([('all','All')] if x.count() else []) + \
            [(item.name, '%s (%d)' % (item.name, item.eps_set.count())) for item in x]

        self.fields['logos'].choices = _choices(Logo.objects.all())

        self.fieldsets.append(
            Fieldset(self, name='', fields=('logos',)))
