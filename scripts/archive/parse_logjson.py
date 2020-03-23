#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import codecs
import django
os.environ["DJANGO_SETTINGS_MODULE"] = 'tour.settings'
django.setup()
from main.models import Tour
from logbuch.models import Logbucheintrag



input = 'media/logbuch/kroatien.json'
tour_alias = 'kroatien'
override = True


def save_log(l):
    tour = Tour.objects.get(alias=tour_alias)
    log, new = Logbucheintrag.objects.get_or_create(tour=tour, tag=l['tag'])
    print('Arbeite an Tag ', l['tag'])
    if 'strecke' in l:
        log.strecke = float(l['strecke'])
    if 'hoehe' in l:
        log.hoehe = float(l['hoehe'])
    if 'zeit' in l:
        log.uptime = float(l['zeit'])
    if 'text' in l:
        log.text = l['text']
    log.save()




# json file sollte auf level eins eine feature collection haben in der alle features (tracks und punkte) sind
with codecs.open(input, 'r', 'utf-8-sig') as f:
    j = json.load(f)
for log in j['logs']:
    save_log(log)
