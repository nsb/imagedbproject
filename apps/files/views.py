# Copyright 2008 - 2009, Niels Sandholt Busch <niels.busch@gmail.com>. All rights reserved.

import os, mimetypes

from django.views.generic.list_detail import object_list, object_detail
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, HttpResponseBadRequest
from django.core.servers.basehttp import FileWrapper
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.conf import settings

from photologue.models import PhotoSizeCache

from models import Image
from forms import imagefilterform_factory

@login_required
@require_http_methods(["GET"])
def list(request, page=1):

    form = imagefilterform_factory(request)()

    return object_list(request,
                       queryset=Image.objects.filter(is_public=True),
                       template_name = 'image_list.html',
                       template_object_name='image',
                       page=page,
                       paginate_by=getattr(settings, 'PAGINATE_BY', 25),
                       extra_context={'form':form})

@login_required
@require_http_methods(["GET"])
def filter(request, page=1):
    form = imagefilterform_factory(request)(request.GET)
    if form.is_valid():

        lookup_args={}
        qs = Image.objects.filter(is_public=True)
        for (key, value) in form.cleaned_data.items():
            if value:
                if value == 'all':
                    pass
                    # ugly hack to get content type, should be fixed
                    model = getattr(Image.objects.get(pk=1), key).model

                    q_object = Q()
                    for value in model.objects.values('name'):
                        q_object = q_object | Q(**{'%s__name' % key: value['name']})
                    qs = qs.filter(q_object).distinct()
                else:
                    lookup_args.update({'%s__name' % key: value})

        qs = qs.filter(**lookup_args)

        return object_list(request,
                           queryset=qs,
                           template_name = 'image_list.html',
                           template_object_name='image',
                           page=page,
                           paginate_by=getattr(settings, 'PAGINATE_BY', 25),
                           extra_context={'form':form, 'query':request.GET.urlencode()})
    else:
        return HttpResponseBadRequest(form.errors)

@login_required
@require_http_methods(["GET"])
def detail(request, image_id):
    return object_detail(request,
                         queryset=Image.objects.filter(is_public=True),
                         template_name = 'image_detail.html',
                         template_object_name = 'image',
                         object_id = image_id)

@login_required
def send_file(request, image_id, size):
    """                                                                         
    Send a file through Django without loading the whole file into              
    memory at once. The FileWrapper will turn the file object into an           
    iterator for chunks of 8KB.                                                 
    """

    image = get_object_or_404(Image, pk=image_id)

    filenames = \
        {'small':image.get_small_filename,
         'medium':image.get_medium_filename,
         'large':image.get_large_filename,
         'original': lambda: image.image.path,}

    if not size in ['original']:
        photosize = PhotoSizeCache().sizes.get(size)
        if photosize and not image.size_exists(photosize):
            image.create_size(photosize)

    filename = filenames[size]()
    mimetype, encoding = mimetypes.guess_type(filename)

    wrapper = FileWrapper(file(filename))
    response = HttpResponse(wrapper, content_type=mimetype or 'image/jpeg')
    response['Content-Length'] = os.path.getsize(filename)
    response['Content-Disposition'] = 'attachment; filename=%s' % os.path.basename(filename)
    return response

