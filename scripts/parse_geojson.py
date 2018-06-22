#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
try:
    import django
    os.environ["DJANGO_SETTINGS_MODULE"] = 'tour.settings'
    django.setup()
    from karte.models import Track
    from main.models import Tour
    from logbuch.models import Logbucheintrag
except:
    print('No django env')



input = 'schweden.json'
tour_alias = 'schweden'

def save_point(geom, tag):
    """Save a point to a related logbuch entry"""
    try:
        tour = Tour.objects.get(alias=tour_alias)
        log = Logbucheintrag.objects.get_or_create(tag=tag, tour=tour)
        log.position = geom  # {'type': 'Point', 'coordinates': [0,0]}
    except:
        print('problem saving a point')




# json file sollte auf level eins eine feature collection haben in der alle features (tracks und punkte) sind
with open(input) as f:
    j = json.load(f)
features = j['features']
print(len(features))

for feat in features:
    print(feat)

    try:
        geom = feat['geometry']
    except:
        print('no geometry, skipping feature')
        continue
    if geom['type'] == 'Point':
        try:
            tag = feat['properties']['name']
            save_point(geom, tag)
        except:
            print('could not safe point')
    elif geom['type'] == 'MultiLineString':
        print('found a track')

