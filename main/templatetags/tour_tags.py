import datetime
from main.models import Tour
from django import template
# import urllib

register = template.Library()

@register.simple_tag
def current_time(format_string):
    return datetime.datetime.now().strftime(format_string)

@register.simple_tag
def touren_liste():
    touren = Tour.objects.filter(listed=True).order_by('date_start').reverse()
    return touren

@register.simple_tag(takes_context=True)
def app_path(context):
    path = context['request'].path
    return path.split('/')[1]
    # return urllib.urlsplit(path_string).path[0]


@register.filter
def lookup(h, key):
    return h[key]
