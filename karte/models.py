from django.db import models
from main.models import Tour
from djgeojson.fields import PointField, MultiLineStringField

# Create your models here.
class Karte(models.Model):
    name = models.CharField(max_length=255, default='unknown')

    def __str__(self):
        return self.name


class Track(models.Model):
    """One day of the tour?"""
    tag = models.IntegerField(null=True, blank=True)
    tour = models.ForeignKey(Tour, on_delete=models.SET_NULL, null=True, blank=True)
    track = MultiLineStringField(null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.tour.name)


class Schlafplatz(models.Model):
    """Punkt an dem wir zelteten"""
    geom = PointField()
    tag = models.IntegerField(null=True, blank=True)
    tour = models.ForeignKey(Tour, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return '{} Tag: {}'.format(self.tour.name, self.tag)
