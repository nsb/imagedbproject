from django.views.generic.list_detail import object_list, object_detail
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import HttpResponseBadRequest

from models import Image
from forms import ImageFilterForm

@login_required
@require_http_methods(["GET"])
def list(request, page=1):

    form = ImageFilterForm()

    return object_list(request,
                       queryset=Image.objects.filter(is_public=True),
                       template_name = 'image_list.html',
                       template_object_name='image',
                       page=page,
                       paginate_by=10,
                       extra_context={'form':form})

@login_required
@require_http_methods(["GET"])
def filter(request, page=1):
    form = ImageFilterForm(request.GET)
    if form.is_valid():
        area = form.cleaned_data['area']
        queryset = Image.objects.filter(is_public=True)

        if area:
            queryset = queryset.filter(area=area)

        return object_list(request,
                           queryset=queryset,
                           template_name = 'image_list.html',
                           template_object_name='image',
                           page=page,
                           paginate_by=10,
                           extra_context={'form':form})
    else:
        return HttpResonseBadRequest(form.errors)



@login_required
@require_http_methods(["GET"])
def detail(request, slug):
    return object_detail(request,
                         queryset=Image.objects.filter(is_public=True),
                         template_name = 'image_detail.html',
                         template_object_name = 'image',
                         slug_field='title_slug',
                         slug=slug,
                         extra_context={})
 