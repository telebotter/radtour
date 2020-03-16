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

    def to_dict(self):
        data = {
            'datum': str(self.datum),
            'text': self.text,
            'tour': self.tour.alias,
            'strecke': self.strecke,
            'uptime': self.uptime,
            'hoehe': self.hoehe,
            'ort': self.ort,}
        return data

    def from_dict(self, data, change=False):
        if not self.tour or (change and hasattr(data, 'tour')):
            tour = Tour.objects.filter(alias=data['tour']).first()
            if tour:
                self.tour = tour
        # TODO shortcut for this primitive fields?
        if not self.datum or change:
            self.datum = data.get('datum', self.datum)
        if not self.text or change:
            self.text = data.get('text', self.text)
        if not self.strecke or change:
            self.strecke = data.get('strecke', self.strecke)
        if not self.hoehe or change:
            self.hoehe = data.get('hoehe', self.hoehe)
        if not self.ort or change:
            self.ort = data.get('ort', self.ort)

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
