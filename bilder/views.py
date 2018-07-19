from django.shortcuts import render, get_object_or_404, get_list_or_404

from bilder.models import Bild
from main.models import Tour


# Create your views here.
def index(request, touralias='kroatien'):
    """All images overview"""
    bilder = get_list_or_404(Bild)
    ctx= {'bilder': bilder}
    return render(request, 'bilder/index.html', context=ctx)


def album(request, touralias):
    tour = get_object_or_404(Tour, alias=touralias)
    context={'tour': tour}
    return render(request, 'bilder/index.html', context=tour)