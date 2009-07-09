# -*- coding: utf-8 -*-
from django.template import Library
     
register = Library()

@register.simple_tag
def in_downloadfolder(img, request):
    try:
        imglist = request.session['image_download_list'] if 'image_download_list' in request.session else []
        imglist.index(str(img))
        return 'checked="yes"'
    except:
        return ''

