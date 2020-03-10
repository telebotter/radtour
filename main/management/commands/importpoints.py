from django.core.management.base import BaseCommand, CommandError
from main.models import Tour
from logbuch.models import Logbucheintrag
import geojson as gj
import datetime as dt

class Command(BaseCommand):
    help = 'enter multilinestring from jsonfile'

    def add_arguments(self, parser):
        parser.add_argument('tour', type=str)
        parser.add_argument('file', type=str)


    def handle(self, *args, **options):
        fpath = options['file']
        tname = options['tour']
        tour = Tour.objects.get(alias=tname)
        self.stdout.write('found tour: {}'.format(tour.name))
        with open(fpath, 'r') as rf:
            collection = gj.load(rf)
        for fet in collection['features']:
            date_str = fet['properties']['date']
            date = dt.datetime.strptime(date_str, '%Y/%m/%d')
            ort = fet['geometry']
            logs = Logbucheintrag.objects.filter(tour=tour, datum=date)
            print(logs)
            if len(logs)==0:
                print('creating entry: {}'.format(date))
                log = Logbucheintrag(datum=date, tour=tour, text='created from geojson', ort=ort)
                log.save()
            elif len(logs)==1:
                if logs[0].ort==None:
                    print('found with empty ort..')
                else:
                    input('ort is not none.. overwrite?')
                logs[0].ort = ort
                logs[0].save()

        #tour.save()
