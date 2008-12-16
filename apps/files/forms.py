from django.forms import ModelForm
from django import forms

from models import Image
from categories.models import Area, Motif, TimeOfDay

class ImageFilterForm(ModelForm):
    areas = forms.ModelChoiceField(queryset=Area.objects.all(), label='Area', required=False)
    motifs = forms.ModelChoiceField(queryset=Motif.objects.all(), label='Motif', required=False)
    times_of_day = forms.ModelChoiceField(queryset=TimeOfDay.objects.all(), label='Time of day', required=False)

    class Meta:
        model = Image
        fields = ('areas', 'motifs', 'times_of_day',)
