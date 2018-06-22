from django.shortcuts import render, get_object_or_404, get_list_or_404
from main.models import Tour
from logbuch.models import Logbucheintrag
from djgeojson.serializers import Serializer as GeoJSONSerializer
from karte.models import Schlafplatz
from django.http import HttpResponse, JsonResponse
# Create your views here.

def index(request):
    context = {}
    context['touren'] = Tour.objects.all()
    return render(request, 'karte/index.html', context=context)


def orte_tour(request, touralias):
    tour = get_object_or_404(Tour, alias=touralias)
    logs = Logbucheintrag.objects.filter(tour=tour)
    points = []
    for log in logs:
        try:
            points.append({'type':'Feature', 'geometry': log.ort, 'properties':{'name': log.tag, 'color': tour.color, 'text': log.text}})
        except Exception as e:
            pass
    geo_json = {'type': 'FeatureCollection', 'features': points, 'properties':{'name': tour.name}}
    context = {}
    context['logs'] = logs
    geoms = Schlafplatz.objects.all()
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