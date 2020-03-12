import datetime
from main.models import Tour
from django import template

register = template.Library()

@register.simple_tag
def current_time(format_string):
    return datetime.datetime.now().strftime(format_string)

@register.simple_tag
def touren_liste():
    touren = Tour.objects.filter(listed=True).order_by('date_start').reverse()
    return touren
