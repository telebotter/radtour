from django.db import models
import datetime as dt
from djgeojson.fields import MultiLineStringField
from colorful.fields import RGBColorField
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill



class Country(models.Model):

    name = models.CharField(max_length=250)
    short = models.CharField(max_length=10)
    lon = models.FloatField(default=0, null=True)
    lat = models.FloatField(default=0, null=True) 
    url = models.CharField(max_length=500, null=True)
    def __str__(self):
        return self.name


class Tour(models.Model):

    name = models.CharField(max_length=250)
    alias = models.CharField(max_length=250, unique=True)  # url-safe
    date_start = models.DateField('Tour Started', null=True)
    track = MultiLineStringField(null=True, blank=True)
    #date_end = models.CharField('Tour Finished', null=True)
    #countries = models.ManyToMany(Country, blank=True)
    color = RGBColorField(default='#000000')
    #length = models.FloatField(blank=True)
    img = models.ImageField(null=True, blank=True)
    img_thumb = ImageSpecField(source='img', processors=[ResizeToFill(100,100)],
                                format='JPEG', options={'quality': 60})
    #tourlog = models.TextField(blank=True)  # html or md content?
    text = models.TextField(blank=True, null=True)
    
    
    def __str__(self):
        """
        Diese Funktion wird automatisch von python/django aufgerufen um 
        ein Objekt zu bennen.
        """
        return self.name
    
    def get_duration(self):
        """
        returns duration of the tour if start and finish date are set correct.
        :return duration: <datetime.timedelta>
        """
        try:
            #duration = date_start - date_end
            duration = 5
        except:
            duration = dt.timedelta(days=0)
        return duration
    
    @property
    def dauer(self):
        """Berechnet die anzahl der tage aus start-enddatum oder anzahl der tagebuch einträge
        """
        try:
            duration = self.date_finish - self.date_start
            days = duration.days
        except:
            from logbuch.models import Logbucheintrag
            logs = Logbucheintrag.objects.filter(tour=self)
            days = len(logs)
        return days

    @property
    def strecke(self):
        """Berechnet strecke als summe aller tageskilometer"""
        from logbuch.models import Logbucheintrag
        logs = Logbucheintrag.objects.filter(tour=self)
        km = 0
        for log in logs:
            try:
                km += log.strecke
            except:
                pass
        return km

    @property
    def hoehe(self):
        """Hoehe als summe aller tagesdaten"""
        from logbuch.models import Logbucheintrag
        logs = Logbucheintrag.objects.filter(tour=self)
        hm = 0
        for log in logs:
            try:
                hm += log.hoehe
            except:
                pass
        return hm



class User(models.Model):
    name = models.CharField(max_length=250, null=True)
    chatid = models.IntegerField()
    date_active = models.DateTimeField('Last Activity', auto_now=True)
    date_signed = models.DateTimeField('User Registred', auto_now=True)

