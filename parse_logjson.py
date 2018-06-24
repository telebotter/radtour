#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import django
os.environ["DJANGO_SETTINGS_MODULE"] = 'tour.settings'
django.setup()
from main.models import Tour
from logbuch.models import Logbucheintrag



input = 'media/logbuch/portugal.json'
tour_alias = 'portugal'
override = True


def save_log(l):
    tour = Tour.objects.get(alias=tour_alias)
    log = Logbucheintrag.objects.get_or_create(tour=tour, tag=log['tag'])
    print('Arbeite an Tag ', l['tag'])
    if 'strecke' in l:
        log.strecke = float(l['strecke'])
    if 'hoehe' in l:
        log.hoehe = float(l['hoehe'])
    if 'zeit' in l:
        log.uptime = float(l['uptime'])
    log.save()




# json file sollte auf level eins eine feature collection haben in der alle features (tracks und punkte) sind
with open(input) as f:
    j = json.load(f)
for log in j['logs']:
    save_log(log)
