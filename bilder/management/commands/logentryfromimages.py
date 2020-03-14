import datetime as dt

from django.core.management.base import BaseCommand, CommandError
from main.models import Tour
from bilder.models import Bild
from logbuch.models import Logbucheintrag


class Command(BaseCommand):
    help = 'pass touralias'

    def add_arguments(self, parser):
        parser.add_argument('tour', type=str)

    def handle(self, *args, **options):
        t = Tour.objects.get(alias=options['tour'])
        start = t.date_start
        bilder = Bild.objects.filter(tour=t)
        for b in bilder:
            print(f'-- {b.date.date()}')
            log, new = Logbucheintrag.objects.get_or_create(tour=t, datum=b.date.date())
            print(f'is new: {new}')
            b.tagebucheintrag = log
            b.save()
