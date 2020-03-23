#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import django
os.environ["DJANGO_SETTINGS_MODULE"] = 'tour.settings'
django.setup()
from main.models import Tour
from logbuch.models import Logbucheintrag

tours = ['kroatien', 'schweden', 'portugal', 'korsika']




def save_track(geom):
    tour = Tour.objects.get(alias=tour_alias)
    tour.track = geom
    tour.save()
    print('track added')

def save_point(geom, tag):
    """Save a point to a related logbuch entry"""
    try:
        tour = Tour.objects.get(alias=tour_alias)
        log, new = Logbucheintrag.objects.get_or_create(tag=tag, tour=tour)
        print(geom)
        log.ort = geom  # {'type': 'Point', 'coordinates': [0,0]}
        log.save()
    except Exception as e:
        print(e)
        print('problem saving a point')



for t in tours:
    input = 'media/karte/tracks/{}.json'.format(t)
    tour_alias = t
    # json file sollte auf level eins eine feature collection haben in der alle features (tracks und punkte) sind
    with open(input) as f:
        j = json.load(f)
    features = j['features']
    print(len(features))

    for feat in features:
        #print(feat)

        try:
            geom = feat['geometry']
        except:
            print('no geometry, skipping feature')
            continue
        if geom['type'] == 'Point':
            try:
                tag = int(feat['properties']['name'])
                print(tag)
                save_point(geom, tag)
            except:
                print('could not safe point')
        elif geom['type'] == 'MultiLineString':
            save_track(geom)
        elif geom['type'] == 'LineString':
            save_track(geom)
