from django.forms import ModelForm
from django import forms

from models import Image
from categories.models import Location, Installation, People, HSE, Event, Graphics, Communications

class ImageFilterForm(ModelForm):
    locations = forms.ModelChoiceField(queryset=Location.objects.all(), label='Locations', required=False)
    installations = forms.ModelChoiceField(queryset=Installation.objects.all(), label='Installations & Vessels', required=False)
    people = forms.ModelChoiceField(queryset=People.objects.all(), label='People', required=False)
    hse = forms.ModelChoiceField(queryset=HSE.objects.all(), label='HSE', required=False)
    events = forms.ModelChoiceField(queryset=Event.objects.all(), label='Events', required=False)
    graphics = forms.ModelChoiceField(queryset=Graphics.objects.all(), label='Graphics', required=False)
    communications = forms.ModelChoiceField(queryset=Communications.objects.all(), label='Communications', required=False)

    class Meta:
        model = Image
        fields = ('locations', 'installations', 'people', 'hse', 'events', 'graphics', 'communications',)
