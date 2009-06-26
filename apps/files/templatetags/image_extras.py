from django.template import Library
     
register = Library()

@register.simple_tag
def in_downloadfolder(img, imglist):
    try:
        imglist.index(str(img))
        return 'checked="yes"'
    except:
        return ''

