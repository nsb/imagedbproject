# Copyright 2008 - 2009, Niels Sandholt Busch <niels.busch@gmail.com>. All rights reserved.

import os
import hashlib
from django.conf import settings

def get_image_path(instance, filename):
    return os.path.join(
        'photos',
        hashlib.md5(''.join(
            (str(instance.date_added.date()),
             settings.SECRET_KEY))).hexdigest().lower(), filename)