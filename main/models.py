from django.db import models
import datetime as dt



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
    alias = models.CharField(max_length=250)  # url-safe
    date_start = models.DateField('Tour Started', auto_now=True)
    date_end = models.CharField('Tour Finished', null=True)
    countries = models.ManyToMany(Country, blank=True)
    color = models.CharField(max_length=10)
    length = models.FloatField(blank=True)
    img = models.ImageField()
    tourlog = models.TextField(blank=True)  # html or md content?
    
    
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
            duration = date_start - date_end
        except:
            duration = dt.timedelta(days=0)
        return duration


class Daylog(models.Model):
    date = models.DateTimeField('Date of the Day', auto_now=True)
    text = models.TextField(blank=True)
    tour = models.ForeignKey(Tour, blank=True)
    length = models.FloatField(blank=True)
    uptime = models.FloatField(blank=True)
    height = models.FloatField(blank=True)
    def __str__(self):
        return str(self.date)



class User(models.Model):
    name = models.CharField(max_length=250, null=True)
    chatid = models.IntegerField()
    date_active = models.DateTimeField('Last Activity', auto_now=True)
    date_signed = models.DateTimeField('User Registred', auto_now=True)

