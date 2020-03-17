from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect
from bilder.models import Bild
from main.models import Tour
from tour.utils import get_exif_date
from bilder.forms import FileFieldForm
import os
from django.conf import settings
from django.contrib.auth.decorators import login_required  # decorator


# Create your views here.
def index(request):
    """All images overview"""
    # apply filter
    tour_alias = request.GET.get('tour', default=False)
    bilder = get_list_or_404(Bild, private=False)
    ctx= {'bilder': bilder}
    return render(request, 'bilder/index.html', context=ctx)


# Create your views here.
def tourgallery(request, alias):
    """All images overview"""
    # apply filter
    # tour_alias = request.GET.get('tour', default=False)
    tour = get_object_or_404(Tour, alias=alias)
    touren = Tour.objects.filter(listed=True)
    bilder = get_list_or_404(Bild, private=False, tour=tour)
    ctx= {'bilder': bilder, 'touren': touren, 'tour': tour}
    #form = FilterForm()
    #ctx['form'] = form
    return render(request, 'bilder/index.html', context=ctx)


@login_required
def upload(request, alias):
    tour = get_object_or_404(Tour, alias=alias)
    if request.method == 'POST':
        form = FileFieldForm(request.POST, request.FILES)
        if form.is_valid():
            for f in request.FILES.getlist('file_field'):
                try:
                    date, fname, tags = get_exif_date(f.file)
                    fpath = os.path.join(settings.MEDIA_ROOT, 'bilder', fname)
                    with open(fpath, 'wb+') as target:
                        # chunk write to save ram for big files
                        for chunk in f.chunks():
                            target.write(chunk)
                    bild, created = Bild.objects.get_or_create(tour=tour, date=date, bild=os.path.join('bilder', fname))
                    if created:
                        messages.info(request, f'datei gespeichert als: {fpath}')
                    else:
                        messages.warning(request, f'bild ist bereits in der db')
                except Exception as e:
                    messages.error(request, f'fehler: {e}')
            #instance = ModelWithFileField(file_field=request.FILES['file'])
            #instance.save()
        else:
            messages.error(request, 'invalid form')
        return HttpResponseRedirect('/bilder/'+tour.alias)
    else:
        form = FileFieldForm()
        return render(request, 'bilder/upload.html', {'form': form, 'tour': tour})
