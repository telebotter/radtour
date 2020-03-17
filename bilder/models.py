from django.db import models
from main.models import Tour
from logbuch.models import Logbucheintrag
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from imagekit.processors import ResizeToFit

# Create your models here.



class Bild(models.Model):
    bild = models.ImageField(null=True, blank=True)
    tour = models.ForeignKey(Tour, null=True, blank=True, on_delete=models.CASCADE)
    tagebucheintrag = models.ForeignKey(Logbucheintrag, null=True, blank=True, on_delete=models.SET_NULL, related_name='bilder')
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
    private = models.BooleanField(default=False)

    def __str__(self):
        return str(self.titel)

    class Meta:
        ordering = ['date', 'bild']
        verbose_name_plural = 'bilder'
