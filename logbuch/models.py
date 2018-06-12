from django.db import models
from main.models import Tour
# Create your models here.


class Logbucheintrag(models.Model):
    """Tagebucheintrag also ein Post zu einem Tag der Tour.
    """
    erstellt = models.DateTimeField('Erstellt am', auto_now_add=True)
    bearbeitet = models.DateTimeField('Bearbeitet am', auto_now=True)
    datum = models.DateTimeField('Datum', null=True, blank=True)
    tag = models.IntegerField('Tag Nummer', null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    tour = models.ForeignKey(Tour, null=True, blank=True,
                             on_delete=models.CASCADE)
    strecke = models.FloatField(null=True, blank=True)
    uptime = models.FloatField(null=True, blank=True)
    hoehe = models.FloatField(null=True, blank=True)
    gps_lon = models.FloatField(null=True, blank=True)
    gps_lat = models.FloatField(null=True, blank=True)


    def __str__(self):
        return str(self.date)