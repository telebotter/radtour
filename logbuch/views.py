import json
from django.http import FileResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, get_list_or_404
from main.models import Tour
from bilder.models import Bild
from logbuch.models import Logbucheintrag
from logbuch.forms import LogForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required  # decorator


@login_required
def list(request, touralias):
    tour = get_object_or_404(Tour, alias=touralias)
    eintraege = Logbucheintrag.objects.filter(tour=tour).order_by('datum')
    context={'tour': tour, 'eintraege': eintraege}
    return render(request, 'logbuch/buch.html', context=context)

"""
@login_required
def tag(request, touralias, tagnummer):
    tour = get_object_or_404(Tour, alias=touralias)
    eintrag = get_object_or_404(Logbucheintrag, tour=tour, tag=tagnummer)
    context={'eintrag':eintrag}
    tagesdatum = eintrag.datum
    #bilder = Bild.objects.filter(date__date=tagesdatum)
    bilder = Bild.objects.filter(date__contains=tagesdatum, labels__in=['pod'])
    context['bilder'] = bilder
    context['anzahl'] = len(bilder)
    return render(request, 'logbuch/tag.html', context=context)
"""

@login_required
def log_edit(request, touralias, log_id):
    tour = get_object_or_404(Tour, alias=touralias)
    log = get_object_or_404(Logbucheintrag, pk=log_id)
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = LogForm(request.POST, instance=log)
        # without instance form.save would create a new log
        # check whether it's valid:
        if form.is_valid():
            # Process data save changes to object.. shortcut for models?
            #log.text = str(request.POST.get('text'))
            #log.hoehe = float(request.POST.get('hoehe'))
            #log.save()
            log = form.save()
            messages.info(request, form.is_bound)
            messages.success(request, log)
            log.save()
            messages.success(request, "Eintrag gespeichert.")
            return HttpResponseRedirect(f'/logbuch/{tour.alias}')
        else:
            #TODO render form validation error
            messages.error(request, "Formulardaten Ungültig. Nicht gespeichert!")
    else: # if a GET create a bound (linked to an instance) form
        form = LogForm(instance=log)

    # add some layout stuff in a dirty way not longer needed see form
    icons = {
        'hoehe': '<i class="fa fa-arrows-v"></i>',
        'uptime': '<i class="fa fa-clock-o"></i>',
        'strecke': '<i class="fa fa-road"></i>',
        'datum': '<i class="fa fa-calendar"></i>',
        'maxspeed': '<i class="fas fa-tachometer-alt"></i>',
        }
    placeholder = {
        'hoehe': 'Anstieg m',
        'uptime': 'Fahrzeit h',
        'strecke': 'Strecke km',
        'datum': 'Datum YYYY-MM-DD',
        'maxspeed': 'Maxges kmh',
    }
    return render(request, 'logbuch/log_edit.html', context={'tour': tour, 'form':form, 'icons': icons, 'placeholder': placeholder, 'log': log})


@login_required
def log_export(request, touralias):
    tour = get_object_or_404(Tour, alias=touralias)
    log_data = [log.to_dict() for log in tour.logs.all()]
    log_json = json.dumps(log_data)
    #return JsonResponse(log_data, safe=False) # PointField is still obj
    response = FileResponse(log_json)
    # Auto detection doesn't work with plain text content, so we set the headers ourselves
    response["Content-Type"] = "text/json"
    response["Content-Length"] = len(log_json)
    response["Content-Disposition"] = 'attachment; filename="' + f'logbuch_{touralias}.json' + '"'
    return response

@login_required
def log_import(request, touralias):
    # TODO uploadjsonfileform
    messages.warning(request, 'Das importieren muss erst noch vernünftig getestet werden, damit nichts ungewollt überschrieben wird. Comming Soon...')
    return(HttpResponseRedirect(f'/logbuch/{touralias}'))
