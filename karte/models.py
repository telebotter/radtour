from django.db import models
from django.db.models import (ForeignKey, IntegerField, FloatField, CharField,
    DateField, BooleanField, OneToOneField, FileField, TimeField)
from django.db.models import (CASCADE, SET_NULL)
from main.models import Tour
from djgeojson.fields import (PointField, MultiLineStringField, LineStringField,
    GeometryField)


# Create your models here.
class Karte(models.Model):
    name = CharField(max_length=255, default='unknown')

    def __str__(self):
        return self.name


class Track(models.Model):
    """ the path with timestamps from one tour, splitted in segments for
    each day. """
    tour = OneToOneField(Tour, on_delete=SET_NULL, auto_created=True, related_name='newtrack', null=True)

    @property
    def geo_json(self):
        data = {
            "type": "FeatureCollection",
            "features": [seg.geo_json for seg in self.segments.all()]}
        return data

    def from_csv(self, csv, force=False):
        return

    def __str__(self):
        return self.tour.name + ' (' + str(self.segments.all().count()) + ')'


class Segment(models.Model):
    name = CharField(max_length=50, null=True, blank=True) # fname from upload
    date = DateField(default='2000-01-01')
    time = TimeField(default='00:00:00')
    line = LineStringField(null=True, blank=True)
    # line_geom = GeometryField(null=True, blank=True)
    transfer = BooleanField(default=False)
    position = FloatField(default=1) # used to order the segments in track
    # TODO: use time field instead of position.. and order bei date, time
    # or just use a datetime field with a default start time of 00:00:00?
    track = ForeignKey(Track, on_delete=SET_NULL, related_name='segments', null=True, blank=True)
    csv = FileField(upload_to='tracks', null=True, blank=True) # not used yet

    def __str__(self):
        return self.name


    @property
    def geo_json(self):
        data = {
            "type": "Feature",
            "geometry": self.line,
            "properties": {
                "transfer": str(self.transfer),
                "date": str(self.date),
                "time": str(self.time),
                "id": str(self.id),
                "popup": f'[{self.id}]<br/>{self.date}<br/>{self.time}<br/>transfer: {self.transfer}</br/><a href="/admin/karte/segment/{self.id}/change/">bearbeiten</a>',
                }
            }
        return data

    def from_csv(self, csv, time='00:00:00', force=False):
        return
