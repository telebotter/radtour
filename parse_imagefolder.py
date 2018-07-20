#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import PIL.Image
import datetime as dt
try:
    import django
    os.environ["DJANGO_SETTINGS_MODULE"] = 'tour.settings'
    django.setup()
    from main.models import Tour
    from logbuch.models import Logbucheintrag
    from bilder.models import Bild
except:
    print('import problem')






tour_alias = 'kroatien'
input = 'media/bilder/'
override = True






def exif_to_dt(path):
    try:
        img = PIL.Image.open(input+fname)
        exif_data = img._getexif()
        datetime = exif_data[36867]
        stamp = dt.datetime.strptime(datetime, '%Y:%m:%d %H:%M:%S')
    except Exception as e:
        print(e)
        stamp = None
    return stamp

def to_db(path, time):
    try:
        bild, new = Bild.objects.get_or_create(bild=path)
        print('new: {}'.format(new))
    except Exception as e:
        print(e)

if __name__ == '__main__':
    for fname in os.listdir(input):
        print(fname)
        name = fname
        time = exif_to_dt(input + fname)
        orig_name = fname
        to_db(fname, time)




