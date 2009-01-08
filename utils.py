import os
import md5
from django.conf import settings

def get_image_path(instance, filename):
    return os.path.join(
        'photos',
        md5.new(''.join(
            (str(instance.date_added.date()),
             settings.SECRET_KEY))).hexdigest().lower(), filename)