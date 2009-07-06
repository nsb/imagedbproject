# -*- coding: utf-8 -*-
# Copyright 2008 - 2009, Niels Sandholt Busch <niels.busch@gmail.com>. All rights reserved.

import os, mimetypes

from django.views.generic.list_detail import object_list, object_detail
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.core.servers.basehttp import FileWrapper
from django.shortcuts import get_object_or_404, render_to_response
from django.db.models import Q
from django.db import models
from django.conf import settings
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from photologue.models import PhotoSizeCache

from models import Image, EPS
from forms import imagefilterform_factory, EPSFilterForm

from categories.models import Communications, Archive

LEADING_PAGE_RANGE_DISPLAYED = TRAILING_PAGE_RANGE_DISPLAYED = 10
LEADING_PAGE_RANGE = TRAILING_PAGE_RANGE = 8
NUM_PAGES_OUTSIDE_RANGE = 2
ADJACENT_PAGES = 4

@require_http_methods(["GET"])
def image_front_reg(request, page=1):

    image_form = imagefilterform_factory(request)()

    return render_to_response('image_front.html', RequestContext(request, {'form':image_form,}))
image_front = login_required( image_front_reg )

@require_http_methods(["GET"])
def images_reg(request, page=1):

    form = imagefilterform_factory(request)(request.GET)
    if form.is_valid():

        lookup_args={}
        qs = Image.objects.filter(is_public=True).order_by('caption', '-date_added')
        for (key, value) in form.cleaned_data.items():
            if value:
                if value == 'all':
                    # ugly hack to get content type, should be fixed
                    model = getattr(Image.objects.get(pk=1), key).model

                    q_object = Q()
                    for value in model.objects.values('name'):
                        q_object = q_object | Q(**{'%s__name' % key: value['name']})
                    qs = qs.filter(q_object).distinct()
                else:
                    lookup_args.update({'%s__name' % key: value})

        qs = qs.filter(**lookup_args)

        # filter communications and archives
        if not request.user.is_staff:
            for value in Communications.objects.values('name'):
                qs = qs.exclude(communications__name=value['name'])
            for value in Archive.objects.values('name'):
                qs = qs.exclude(archives__name=value['name'])

        image_paginator = Paginator(qs, getattr(settings, 'PAGINATE_BY', 25))

        try:
            images = image_paginator.page(page)
        except (EmptyPage, InvalidPage):
            images = image_paginator.page(image_paginator.num_pages)
 
        " Initialize variables "
        in_leading_range = in_trailing_range = False
        pages_outside_leading_range = pages_outside_trailing_range = range(0)
 
        page = images

        if (page.paginator.num_pages <= LEADING_PAGE_RANGE_DISPLAYED):
            in_leading_range = in_trailing_range = True
            page_numbers = page.paginator.page_range
        elif (page.number <= LEADING_PAGE_RANGE):
            in_leading_range = True
            page_numbers = [n for n in range(1, LEADING_PAGE_RANGE_DISPLAYED + 1) if n > 0 and n <= page.paginator.num_pages]
            pages_outside_leading_range = [n + page.paginator.num_pages for n in range(0, -NUM_PAGES_OUTSIDE_RANGE, -1)]
        elif (page.number > page.paginator.num_pages - TRAILING_PAGE_RANGE):
            in_trailing_range = True
            page_numbers = [n for n in range(page.paginator.num_pages - TRAILING_PAGE_RANGE_DISPLAYED + 1, page.paginator.num_pages + 1) if n > 0 and n <= page.paginator.num_pages]
            pages_outside_trailing_range = [n + 1 for n in range(0, NUM_PAGES_OUTSIDE_RANGE)]
        else: 
            page_numbers = [n for n in range(page.number - ADJACENT_PAGES, page.number + ADJACENT_PAGES + 1) if n > 0 and n <= page.paginator.num_pages]
            pages_outside_leading_range = [n + page.paginator.num_pages for n in range(0, -NUM_PAGES_OUTSIDE_RANGE, -1)]
            pages_outside_trailing_range = [n + 1 for n in range(0, NUM_PAGES_OUTSIDE_RANGE)]
        context = {
            "page_numbers": page_numbers,
            "in_leading_range" : in_leading_range,
            "in_trailing_range" : in_trailing_range,
            "pages_outside_leading_range": pages_outside_leading_range,
            "pages_outside_trailing_range": pages_outside_trailing_range
        }

        context.update(
            {'images':images,
             'form':form,
             'query':request.GET.urlencode()})

        return render_to_response(
            'image_list.html',
            RequestContext(
                request,
                context))

    else:
        return HttpResponseBadRequest(form.errors)
images = login_required( images_reg )

@require_http_methods(["GET"])
def image_detail_reg(request, image_id):
    return object_detail(request,
                         queryset=Image.objects.filter(is_public=True),
                         template_name = 'image_detail.html',
                         template_object_name = 'image',
                         object_id = image_id)
image_detail = login_required( image_detail_reg )

def image_downloadfolder_view_reg(request, page=1):
    """
    Display list of images selected for download
    """
    
    download_list = request.session.get('image_download_list', [])
    qs = Image.objects.filter(id__in=download_list)
    
    # the rest should be abstracted and generic
    
    # filter communications and archives
    if not request.user.is_staff:
        for value in Communications.objects.values('name'):
            qs = qs.exclude(communications__name=value['name'])
        for value in Archive.objects.values('name'):
            qs = qs.exclude(archives__name=value['name'])

    image_paginator = Paginator(qs, getattr(settings, 'PAGINATE_BY', 25))

    try:
        images = image_paginator.page(page)
    except (EmptyPage, InvalidPage):
        images = image_paginator.page(image_paginator.num_pages)

    " Initialize variables "
    in_leading_range = in_trailing_range = False
    pages_outside_leading_range = pages_outside_trailing_range = range(0)

    page = images

    if (page.paginator.num_pages <= LEADING_PAGE_RANGE_DISPLAYED):
        in_leading_range = in_trailing_range = True
        page_numbers = page.paginator.page_range
    elif (page.number <= LEADING_PAGE_RANGE):
        in_leading_range = True
        page_numbers = [n for n in range(1, LEADING_PAGE_RANGE_DISPLAYED + 1) if n > 0 and n <= page.paginator.num_pages]
        pages_outside_leading_range = [n + page.paginator.num_pages for n in range(0, -NUM_PAGES_OUTSIDE_RANGE, -1)]
    elif (page.number > page.paginator.num_pages - TRAILING_PAGE_RANGE):
        in_trailing_range = True
        page_numbers = [n for n in range(page.paginator.num_pages - TRAILING_PAGE_RANGE_DISPLAYED + 1, page.paginator.num_pages + 1) if n > 0 and n <= page.paginator.num_pages]
        pages_outside_trailing_range = [n + 1 for n in range(0, NUM_PAGES_OUTSIDE_RANGE)]
    else: 
        page_numbers = [n for n in range(page.number - ADJACENT_PAGES, page.number + ADJACENT_PAGES + 1) if n > 0 and n <= page.paginator.num_pages]
        pages_outside_leading_range = [n + page.paginator.num_pages for n in range(0, -NUM_PAGES_OUTSIDE_RANGE, -1)]
        pages_outside_trailing_range = [n + 1 for n in range(0, NUM_PAGES_OUTSIDE_RANGE)]
    context = {
        "page_numbers": page_numbers,
        "in_leading_range" : in_leading_range,
        "in_trailing_range" : in_trailing_range,
        "pages_outside_leading_range": pages_outside_leading_range,
        "pages_outside_trailing_range": pages_outside_trailing_range
    }

    return render_to_response(
        'image_download_list.html', RequestContext(request, 
        {'images':images}))
image_downloadfolder_view = login_required( image_downloadfolder_view_reg )
    
@require_http_methods(["GET"])  
def image_downloadfolder_download_reg(request):
    """
    Compresses images from the download folder in a zip archive
    and sends it. The FileWrapper will turn the file object into an           
    iterator for chunks of 8KB.
    """
    size = request.GET.get('size', 'medium')
    download_list = request.session.get('image_download_list', [])
    qs = Image.objects.filter(id__in=download_list)
        
    temp = tempfile.TemporaryFile()
    archive = zipfile.ZipFile(temp, 'w', zipfile.ZIP_DEFLATED)
    
    for image in qs:  
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
        archive.write(filename)
       
    archive.close()
    wrapper = FileWrapper(temp)
    response = HttpResponse(wrapper, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=images.zip'
    response['Content-Length'] = temp.tell()
    temp.seek(0)
    return response 
image_downloadfolder_download = login_required( image_downloadfolder_download_reg )

@require_http_methods(["POST"])
def image_downloadfolder_update_reg(request):
    """
    Updates the download folder. Removes all images in the selection view
    from the session variable, then ads the images that have been ticked off
    """
    
    img_all = request.POST.get('img_all', '').split(',')
    selected = request.POST.getlist('img_down')
    download_list = request.session.get('image_download_list', [])

    for img in img_all:
        try: 
            download_list.remove(img)
        except:
            pass 
    
    download_list.extend(selected)
    request.session['image_download_list'] = download_list
    
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
image_downloadfolder_update = login_required( image_downloadfolder_update_reg )

def image_downloadfolder_clear_reg(request):
    request.session['image_download_list'] = []
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
image_downloadfolder_clear = login_required( image_downloadfolder_clear_reg )

@require_http_methods(["POST"])
def image_downloadfolder_toggle_reg(request):
    img = request.POST.get('img', '')
    pass
image_downloadfolder_toggle = login_required( image_downloadfolder_toggle_reg )

def send_image_reg(request, image_id, size):
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
    response = HttpResponse(wrapper, content_type='%s; charset=utf8' % mimetype or 'image/jpeg')
    response['Content-Length'] = os.path.getsize(filename.encode('utf8'))
    response['Content-Disposition'] = 'attachment; filename=%s' % os.path.basename(filename.encode('utf8'))
    return response
send_image = login_required( send_image_reg )

@require_http_methods(["GET"])
def eps_front_reg(request, page=1):

    eps_form = EPSFilterForm()

    return render_to_response('eps_front.html', RequestContext(request, {'form':eps_form,}))
eps_front = login_required( eps_front_reg )

def eps(request, page=1):

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

        " Initialize variables "
        in_leading_range = in_trailing_range = False
        pages_outside_leading_range = pages_outside_trailing_range = range(0)
 
        page = eps

        if (page.paginator.num_pages <= LEADING_PAGE_RANGE_DISPLAYED):
            in_leading_range = in_trailing_range = True
            page_numbers = page.paginator.page_range
        elif (page.number <= LEADING_PAGE_RANGE):
            in_leading_range = True
            page_numbers = [n for n in range(1, LEADING_PAGE_RANGE_DISPLAYED + 1) if n > 0 and n <= page.paginator.num_pages]
            pages_outside_leading_range = [n + page.paginator.num_pages for n in range(0, -NUM_PAGES_OUTSIDE_RANGE, -1)]
        elif (page.number > page.paginator.num_pages - TRAILING_PAGE_RANGE):
            in_trailing_range = True
            page_numbers = [n for n in range(page.paginator.num_pages - TRAILING_PAGE_RANGE_DISPLAYED + 1, page.paginator.num_pages + 1) if n > 0 and n <= page.paginator.num_pages]
            pages_outside_trailing_range = [n + 1 for n in range(0, NUM_PAGES_OUTSIDE_RANGE)]
        else: 
            page_numbers = [n for n in range(page.number - ADJACENT_PAGES, page.number + ADJACENT_PAGES + 1) if n > 0 and n <= page.paginator.num_pages]
            pages_outside_leading_range = [n + page.paginator.num_pages for n in range(0, -NUM_PAGES_OUTSIDE_RANGE, -1)]
            pages_outside_trailing_range = [n + 1 for n in range(0, NUM_PAGES_OUTSIDE_RANGE)]
        context = {
            "page_numbers": page_numbers,
            "in_leading_range" : in_leading_range,
            "in_trailing_range" : in_trailing_range,
            "pages_outside_leading_range": pages_outside_leading_range,
            "pages_outside_trailing_range": pages_outside_trailing_range
        }

        context.update(
            {'eps':eps,
                 'form':form,
                 'query':request.GET.urlencode()})

        return render_to_response(
            'eps_list.html',
            RequestContext(
                request,
                context))

    else:
        return HttpResponseBadRequest(form.errors)

@require_http_methods(["GET"])
def eps_detail_reg(request, eps_id):
    return object_detail(request,
                         queryset=EPS.objects.filter(is_public=True),
                         template_name = 'eps_detail.html',
                         template_object_name = 'eps',
                         object_id = eps_id)
eps_detail = login_required( eps_detail_reg )

def send_eps_reg(request, eps_id):
    """                                                                         
    Send a file through Django without loading the whole file into              
    memory at once. The FileWrapper will turn the file object into an           
    iterator for chunks of 8KB.                                                 
    """

    eps = get_object_or_404(EPS, pk=eps_id)

    filename = eps.eps.path

    mimetype, encoding = mimetypes.guess_type(filename)

    wrapper = FileWrapper(file(filename))
    response = HttpResponse(wrapper, content_type=mimetype or 'application/postscript')
    response['Content-Length'] = os.path.getsize(filename.encode('utf8'))
    response['Content-Disposition'] = 'attachment; filename=%s' % os.path.basename(filename.encode('utf8'))
    return response
send_eps = login_required( send_eps_reg )

def send_cmyk_reg(request, eps_id):
    """                                                                         
    Send a file through Django without loading the whole file into              
    memory at once. The FileWrapper will turn the file object into an           
    iterator for chunks of 8KB.                                                 
    """

    eps = get_object_or_404(EPS, pk=eps_id)

    filename = eps.cmyk.path

    mimetype, encoding = mimetypes.guess_type(filename)

    wrapper = FileWrapper(file(filename))
    response = HttpResponse(wrapper, content_type=mimetype or 'application/postscript')
    response['Content-Length'] = os.path.getsize(filename.encode('utf8'))
    response['Content-Disposition'] = 'attachment; filename=%s' % os.path.basename(filename.encode('utf8'))
    return response
send_cmyk = login_required( send_cmyk_reg )

def send_pantone_reg(request, eps_id):
    """                                                                         
    Send a file through Django without loading the whole file into              
    memory at once. The FileWrapper will turn the file object into an           
    iterator for chunks of 8KB.                                                 
    """

    eps = get_object_or_404(EPS, pk=eps_id)

    filename = eps.pantone.path

    mimetype, encoding = mimetypes.guess_type(filename)

    wrapper = FileWrapper(file(filename))
    response = HttpResponse(wrapper, content_type=mimetype or 'application/postscript')
    response['Content-Length'] = os.path.getsize(filename.encode('utf8'))
    response['Content-Disposition'] = 'attachment; filename=%s' % os.path.basename(filename.encode('utf8'))
    return response
send_pantone = login_required( send_pantone_reg )

def bulk_caption_reg(request, app_label, model_name):
    """
    Intermediate view for admin action that allows
    bulk edits of captions for both the Image and EPS model
    """

    
    ids = request.GET[u'ids'].split(',')
    
    model = models.get_model(app_label, model_name)
    qs = model.objects.filter(id__in=ids)

    
    if request.method == 'POST':
        bulkcaption = request.POST[u'caption']
          
        qs.update(caption=bulkcaption)
        request.user.message_set.create(
            message="Succesfully changed the caption of %s images." % qs.count())
        return HttpResponseRedirect("../")
        
    else:
        return render_to_response('admin/bulk_caption.html', 
            RequestContext(request, {'object_list': qs,
                'title': 'Bulk update of captions',}))
bulk_caption = staff_member_required( bulk_caption_reg )

def login_reg(request):
    return HttpResponseRedirect( getattr( request.REQUEST, 'next', '/' ) )
