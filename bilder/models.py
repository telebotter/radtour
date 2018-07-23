from django.db import models
from main.models import Tour
from logbuch.models import Logbucheintrag
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from imagekit.processors import ResizeToFit

# Create your models here.

class Label(models.Model):
    private = models.BooleanField(default=False)
    name = models.CharField(max_length=50, primary_key=True)




class Bild(models.Model):
    bild = models.ImageField(null=True, blank=True)
    tour = models.ForeignKey(Tour, null=True, blank=True, on_delete=models.CASCADE)
    tagebucheintrag = models.ForeignKey(Logbucheintrag, null=True, blank=True, on_delete=models.SET_NULL)
    bewertung = models.FloatField(null=True, blank=True)  # 0-1
    titel = models.CharField(null=True, max_length=255, blank=True)
    kommentar = models.CharField(null=True, max_length=255, blank=True)
    date = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    bild_web = ImageSpecField(source='bild',
                                      processors=[ResizeToFit(1000, 1000)],
                                      format='JPEG',
                                      options={'quality': 90})
    bild_thumb = ImageSpecField(source='bild', processors=[ResizeToFill(100,100)],
                                format='JPEG', options={'quality': 60})
    labels = models.ManyToManyField(Label, blank=True, null=True, related_name='bild_label')
    private = models.BooleanField(default=False)

