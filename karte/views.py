from django.shortcuts import render, get_object_or_404, get_list_or_404
from main.models import Tour
# from karte.forms import FileFieldForm
from logbuch.models import Logbucheintrag
from karte.forms import FileFieldForm
from karte.models import Segment, Track
from djgeojson.serializers import Serializer as GeoJSONSerializer
# from karte.models import Schlafplatz
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required  # decorator
from django.contrib import messages
import os
from django.conf import settings
import pandas as pd
import numpy as np
import geojson as gj
import datetime as dt
from django.utils.safestring import mark_safe
import shutil
from uuid import uuid4


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


@login_required
def split_segment(request, seg, lat, lon):
    # tour = get_object_or_404(Tour, alias=touralias)
    segment = get_object_or_404(Segment, pk=seg)
    tour = segment.track.tour
    csv_file = os.path.join(settings.MEDIA_ROOT, segment.csv.path)
    df = pd.read_csv(csv_file)
    df['dist'] = np.abs(df['Latitude']-float(lat)) + np.abs(df['Longitude']-float(lon))
    imin = np.argmin(df['dist'])
    df_old = df.iloc[0:imin+1]
    df_new = df.iloc[imin:-1]
    if request.GET.get('confirmed', False):
        # backup old entry
        csv_bak = segment.csv.path + '.bak'+str(uuid4())
        shutil.copyfile(csv_file, os.path.join(settings.MEDIA_ROOT, csv_bak))

        if request.GET.get('shift', False) == 'time':
            times = pd.to_datetime(df_new['Time'], format='%H:%M:%S')
            times += dt.timedelta(hours=1)
            df_new['Time'] = times.apply(lambda x: x.strftime('%H:%M:%S'))
            messages.info(request, str(df['Time']))
        if request.GET.get('shift', False) == 'date':
            dates = pd.to_datetime(df_new['Date'], format='%Y-%m-%d')
            dates += dt.timedelta(days=1)
            df_new["Date"] = dates.apply(lambda x: x.strftime("%Y-%m-%d"))
            messages.info(request, str(df['Date']))
        # old_seg = Segment.objects.create()
        # old_seg_f = df_old['Date'].iloc[0].replace('-', '') + '_' + str(uuid4()) + '.csv'
        # df_old.to_csv(os.path.join(settings.MEDIA_ROOT, 'tracks', old_seg_f, index=False, sep=',')
        # old_seg.csv = os.path.join('tracks, old_seg')
        # # TODO: set all properties and geojson and same for new seg
        #
        # # disable old entry
        # segment.csv = csv_bak
        # segment.track = None
        # segment.save()
        return render(request, 'karte/splitseg.html')



    messages.info(request, f'{str(imin)} von {len(df)} ({imin/len(df)*100:.1f}%) lat+lon abst zu track: {df["dist"].iloc[imin]:.3g}')
    messages.info(request, f'Datum: {df["Date"].iloc[0]} ... {df["Date"].iloc[imin]} ... {df["Date"].iloc[-1]}')
    messages.info(request, f'Uhrzeit: {df["Time"].iloc[0]} ... {df["Time"].iloc[imin]} ... {df["Time"].iloc[-1]}')
    if df["Time"].iloc[0] == df["Time"].iloc[-1]:
        messages.warning(request, 'Achtung es sieht aus als würden Zeitstempel fehlen. Eventuell sollte das neue Segment verschoben werden, damit die Reihenfolge erhalten bleibt.')

    return render(request, 'karte/splitseg.html')


@login_required
def upload(request, touralias):
    tour = get_object_or_404(Tour, alias=touralias)
    if request.method == 'POST':
        form = FileFieldForm(request.POST, request.FILES)
        if form.is_valid():
            for f in request.FILES.getlist('file_field'):
                try:
                    fpath = os.path.join(settings.MEDIA_ROOT, 'tracks', f.name)
                    with open(fpath, 'wb+') as target:
                        # chunk write to save ram for big files
                        for chunk in f.chunks():
                            target.write(chunk)
                    messages.info(request, f'datei gespeichert als: {fpath}')
                    df = pd.read_csv(fpath, sep=',')
                    date_str = df['Date'][0]
                    date = date_str.replace('/', '-')
                    time = df['Time'][0]
                    # TODO: check file or date/time? or is name good
                    track, created = Track.objects.get_or_create(tour=tour)
                    seg, created = Segment.objects.get_or_create(name=f.name, track=track, date=date, time=time)
                    if created:
                        # coords = df[['Longitude', 'Latitude', 'Alt', 'Time']].values
                        coords = df[['Longitude', 'Latitude']].values
                        gj_line = gj.LineString([(c[0],c[1]) for c in coords])
                        print(gj_line)
                        seg.line = gj_line
                        seg.csv = os.path.join('tracks', f.name)
                        seg.save()
                        messages.info(request, f'Neues Segment {f.name} erstellt.')
                    else:
                        messages.warning(request, f'<a href="/admin/karte/segments/{seg.id}/change">Segment {f.name}</a> bereits vorhanden, kann über django admin <a href="/admin/karte/segments/{seg.id}/delete">gelöscht werden</a>.')
                except Exception as e:
                    if settings.DEBUG:
                        messages.error(request, f'fehler: {e}')
                    else:
                        messages.error(request, 'Ein Fehler ist aufgetreten, Fehlermeldung nur bei DEBUG=True')
            #instance = ModelWithFileField(file_field=request.FILES['file'])
            #instance.save()
        else:
            messages.error(request, 'invalid form')
        return HttpResponseRedirect('/karte/'+tour.alias+'/upload')
    else:
        form = FileFieldForm()
        return render(request, 'karte/upload.html', {'form': form, 'tour': tour})
