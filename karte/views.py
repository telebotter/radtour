from django.shortcuts import render, get_object_or_404, get_list_or_404
from main.models import Tour
# from karte.forms import FileFieldForm
from logbuch.models import Logbucheintrag
from djgeojson.serializers import Serializer as GeoJSONSerializer
# from karte.models import Schlafplatz
from django.http import HttpResponse, JsonResponse
# Create your views here.

def index(request):
    context = {}
    context['touren'] = Tour.objects.all()
    return render(request, 'karte/karte.html', context=context)


def index_tour(request, touralias):
    context = {}
    context['touren'] = Tour.objects.all()
    context['tour'] = get_object_or_404(Tour, alias=touralias)
    return render(request, 'karte/karte.html', context=context)


def orte_tour(request, touralias):
    tour = get_object_or_404(Tour, alias=touralias)
    logs = Logbucheintrag.objects.filter(tour=tour)
    points = []
    for log in logs:
        if user.is_authenticated:
            text = log.text
        else:
            text = 'Logbucheinträge nur mit Login!'
        try:
            points.append({'type':'Feature', 'geometry': log.ort, 'properties':{'name': log.datum, 'color': tour.color, 'text': text, 'date': log.datum}})
        except Exception as e:
            pass
    geo_json = {'type': 'FeatureCollection', 'features': points, 'properties':{'name': tour.name}}
    context = {}
    context['logs'] = logs
    # geoms = Schlafplatz.objects.all()
    #json = GeoJSONSerializer().serialize(Schlafplatz.objects.all(),
    #                              use_natural_keys=True, with_modelname=False)

    #return HttpResponse(json, content_type="application/json")
    return JsonResponse(geo_json)


def track_tour(request, touralias):
    tour = get_object_or_404(Tour, alias=touralias)
    track = tour.track
    data = {'type':'Feature', 'geometry': track, 'properties':{'name': tour.name, 'color': tour.color}}
    geo_json = {'type': 'FeatureCollection', 'features': [data]}
    json = GeoJSONSerializer().serialize(data)
    #return HttpResponse(json, content_type='application/json')
    return JsonResponse(geo_json)


def new_track(request, touralias):
    tour = get_object_or_404(Tour, alias=touralias)
    #track = tour.newtrack
    return JsonResponse(tour.newtrack.geo_json)


# @login_required
# def upload_csv(request, touralias):
#     tour = get_object_or_404(Tour, alias=touralias)
#     if request.method == 'POST':
#         form = FileFieldForm(request.POST, request.FILES)
#         if form.is_valid():
#             for f in request.FILES.getlist('file_field'):
#                 try:
#                     date, fname, tags = get_exif_date(f.file)
#                     fpath = os.path.join(settings.MEDIA_ROOT, 'bilder', fname)
#                     with open(fpath, 'wb+') as target:
#                         # chunk write to save ram for big files
#                         for chunk in f.chunks():
#                             target.write(chunk)
#                     bild, created = Bild.objects.get_or_create(tour=tour, date=date, bild=os.path.join('bilder', fname))
#                     if created:
#                         messages.info(request, f'datei gespeichert als: {fpath}')
#                     else:
#                         messages.warning(request, f'bild ist bereits in der db')
#                 except Exception as e:
#                     messages.error(request, f'fehler: {e}')
#             #instance = ModelWithFileField(file_field=request.FILES['file'])
#             #instance.save()
#         else:
#             messages.error(request, 'invalid form')
#         return HttpResponseRedirect('/bilder/'+tour.alias)
#     else:
#         form = FileFieldForm()
#         return render(request, 'bilder/upload.html', {'form': form, 'tour': tour})
