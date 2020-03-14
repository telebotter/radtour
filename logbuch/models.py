from django.db import models
from main.models import Tour
from djgeojson.fields import PointField
# Create your models here.


class Logbucheintrag(models.Model):
    """Tagebucheintrag also ein Post zu einem Tag der Tour.
    """
    erstellt = models.DateTimeField('Erstellt am', auto_now=True)
    bearbeitet = models.DateTimeField('Bearbeitet am', auto_now=True)
    datum = models.DateField('Datum')
    tag = models.IntegerField('Tag Nummer', null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    tour = models.ForeignKey(Tour, null=True, blank=True,
                             on_delete=models.CASCADE, related_name='logs')
    strecke = models.FloatField(null=True, blank=True)
    uptime = models.FloatField(null=True, blank=True)
    hoehe = models.FloatField(null=True, blank=True)
    ort = PointField(null=True, blank=True)


    @property
    def naechster_eintrag(self):
        try:
            next = self.tag +1
        except:
            next = 0
        return next

    @property
    def letzter_eintrag(self):
        try:
            prev = self.tag -1
        except:
            prev = 0
        return prev


    def __str__(self):
        try:
            return str('{}: Tag {} ({})'.format(self.tour.name, str(self.tag), str(self.datum)))
        except:
            try:
                return str('{}: {}'.format(self.tour.name, self.datum))
            except:
                return str(self.datum)
