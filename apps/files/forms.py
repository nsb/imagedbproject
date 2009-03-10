# Copyright 2008 - 2009, Niels Sandholt Busch <niels.busch@gmail.com>. All rights reserved.

from django.forms import ModelForm
from django import forms

from models import Image
from categories.models import Location, Field, Installation, People, HSE, Event, Graphics, Communications, Archive

class ImageFilterForm(ModelForm):
    locations = forms.ChoiceField(label='Locations', required=False)
    fields = forms.ChoiceField(label='Fields', required=False)
    installations = forms.ChoiceField(label='Installations & Vessels', required=False)
    people = forms.ChoiceField(label='People', required=False)
    hse = forms.ChoiceField(label='HSE', required=False)
    events = forms.ChoiceField(label='Events', required=False)
    graphics = forms.ChoiceField(label='Graphics', required=False)
    communications = forms.ChoiceField(label='Communications use only', required=False)
    archives = forms.ChoiceField(label='Archives', required=False)

    def __init__(self, *args, **kwargs):
        super(ImageFilterForm, self).__init__(*args, **kwargs)

        _choices = lambda x: [('','')] + ([('all','All')] if x.count() else []) + \
            [(item.name, '%s (%d)' % (item.name, item.image_set.count())) for item in x]

        self.fields['locations'].choices = _choices(Location.objects.all())
        self.fields['fields'].choices = _choices(Field.objects.all())
        self.fields['installations'].choices = _choices(Installation.objects.all())
        self.fields['people'].choices = _choices(People.objects.all())
        self.fields['hse'].choices = _choices(HSE.objects.all())
        self.fields['events'].choices = _choices(Event.objects.all())
        self.fields['graphics'].choices = _choices(Graphics.objects.all())
        self.fields['communications'].choices = _choices(Communications.objects.all())
        self.fields['archives'].choices = _choices(Archive.objects.all())

    class Meta:
        model = Image
        fields = ('locations', 'fields', 'installations', 'people', 'hse', 'events', 'graphics', 'communications', 'archives',)
