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






tour_alias = 'korsika'
ipath = 'media/bilder/'
apath = 'bilder/'  # media path is used by default for images?
override = True






def exif_to_dt(path):
    try:
        img = PIL.Image.open(ipath+fname)
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
        if new:
            bild.date = time
            if time:
                bild.titel = dt.datetime.strftime(time, '%Y-%m-%d_%H-%M-%S')
            else:
                bild.titel = path.split('/')[-1]
            try:
                bild.tour = Tour.objects.get(alias=tour_alias)
            except:
                print('tour not found: {}'.format(tour_alias))
            bild.save()
        else:
            print('skipping existing entry: {}'.format(path))
    except Exception as e:
        print(e)

if __name__ == '__main__':
    for fname in os.listdir(ipath):
        
        print(fname)
        if not fname[-3:] in ['jpg', 'JPG', 'peg', 'PEG']:
            print('no jpg')
            continue
        name = fname
        time = exif_to_dt(ipath + fname)
        orig_name = fname
        to_db(apath+fname, time)
        




