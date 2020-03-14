import datetime as dt

from django.core.management.base import BaseCommand, CommandError
from main.models import Tour
from logbuch.models import Logbucheintrag


class Command(BaseCommand):
    help = 'pass touralias'

    def add_arguments(self, parser):
        parser.add_argument('tour', type=str)

    def handle(self, *args, **options):
        t = Tour.objects.get(alias=options['tour'])
        start = t.date_start
        logs = t.logs.all()
        for log in logs:
            tage = log.tag -1
            log_tag = start + dt.timedelta(days=tage)
            log.datum = log_tag
            log.save()
