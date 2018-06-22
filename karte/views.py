from django.shortcuts import render, get_object_or_404, get_list_or_404
from main.models import Tour
from karte.models import Schlafplatz
from django.http import HttpResponse
# Create your views here.

def index(request):
    schlaf_plaetze = get_list_or_404(Schlafplatz)
    return