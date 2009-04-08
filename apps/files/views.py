# Copyright 2008 - 2009, Niels Sandholt Busch <niels.busch@gmail.com>. All rights reserved.

import os, mimetypes

from django.views.generic.list_detail import object_list, object_detail
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, HttpResponseBadRequest
from django.core.servers.basehttp import FileWrapper
from django.shortcuts import get_object_or_404, render_to_response
from django.db.models import Q
from django.conf import settings
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from photologue.models import PhotoSizeCache

from models import Image, EPS
from forms import imagefilterform_factory, EPSFilterForm

@login_required
@require_http_methods(["GET"])
def list(request, page=1):

    image_form = imagefilterform_factory(request)()
    image_list = Image.objects.select_related().filter(is_public=True)
    image_paginator = Paginator(image_list, getattr(settings, 'PAGINATE_BY', 25))

    try:
        images = image_paginator.page(page)
    except (EmptyPage, InvalidPage):
        images = image_paginator.page(image_paginator.num_pages)

    eps_form = EPSFilterForm()
    eps_list = EPS.objects.select_related().all()
    eps_paginator = Paginator(eps_list, getattr(settings, 'PAGINATE_BY', 25))

    try:
        eps = eps_paginator.page(page)
    except (EmptyPage, InvalidPage):
        eps = eps_paginator.page(eps_paginator.num_pages)

    return render_to_response(
        'list.html',
        RequestContext(request,
            {'image_form':image_form,
             'images':images,
             'eps_form':eps_form,
             'eps':eps}))

@login_required
@require_http_methods(["GET"])
def images(request, page=1):

    eps_form = EPSFilterForm()
    eps_list = EPS.objects.select_related().filter(is_public=True)
    eps_paginator = Paginator(eps_list, getattr(settings, 'PAGINATE_BY', 25))

    try:
        eps = eps_paginator.page(1)
    except (EmptyPage, InvalidPage):
        eps = eps_paginator.page(eps_paginator.num_pages)

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

        image_paginator = Paginator(qs, getattr(settings, 'PAGINATE_BY', 25))

        try:
            images = image_paginator.page(page)
        except (EmptyPage, InvalidPage):
            images = image_paginator.page(image_paginator.num_pages)

        return render_to_response(
            'image_list.html',
            RequestContext(
                request,
                {'images':images,
                 'image_form':form,
                 'eps':eps,
                 'eps_form':eps_form,
                 'query':request.GET.urlencode()}))

    else:
        return HttpResponseBadRequest(form.errors)

@login_required
@require_http_methods(["GET"])
def image_detail(request, image_id):
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

def eps(request, page=1):

    image_form = imagefilterform_factory(request)()
    image_list = Image.objects.select_related().filter(is_public=True)
    image_paginator = Paginator(image_list, getattr(settings, 'PAGINATE_BY', 25))

    try:
        images = image_paginator.page(1)
    except (EmptyPage, InvalidPage):
        images = image_paginator.page(image_paginator.num_pages)

    form = EPSFilterForm(request.GET)
    if form.is_valid():

        lookup_args={}
        qs = EPS.objects.all()
        for (key, value) in form.cleaned_data.items():
            if value:
                if value == 'all':
                    pass
                    # ugly hack to get content type, should be fixed
                    model = getattr(EPS.objects.get(pk=1), key).model

                    q_object = Q()
                    for value in model.objects.values('name'):
                        q_object = q_object | Q(**{'%s__name' % key: value['name']})
                    qs = qs.filter(q_object).distinct()
                else:
                    lookup_args.update({'%s__name' % key: value})

        qs = qs.filter(**lookup_args)

        eps_paginator = Paginator(qs, getattr(settings, 'PAGINATE_BY', 25))

        try:
            eps = eps_paginator.page(page)
        except (EmptyPage, InvalidPage):
            eps = eps_paginator.page(eps_paginator.num_pages)

        return render_to_response(
            'eps_list.html',
            RequestContext(
                request,
                {'eps':eps,
                 'eps_form':form,
                 'images':images,
                 'image_form':image_form,
                 'query':request.GET.urlencode()}))

    else:
        return HttpResponseBadRequest(form.errors)


@login_required
@require_http_methods(["GET"])
def eps_detail(request, eps_id):
    return object_detail(request,
                         queryset=EPS.objects.filter(is_public=True),
                         template_name = 'eps_detail.html',
                         template_object_name = 'eps',
                         object_id = eps_id)
