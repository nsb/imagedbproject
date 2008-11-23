from django.forms import ModelForm

from models import Image

class ImageFilterForm(ModelForm):
    class Meta:
        model = Image
        fields = ('area', 'motif', 'time_of_day',)