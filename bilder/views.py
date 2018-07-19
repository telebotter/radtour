from django.shortcuts import render, get_object_or_404, get_list_or_404

from bilder.models import Bild


# Create your views here.
def index(request):
    """All images overview"""
    bilder = get_list_or_404(Bild)
    return render(request, 'bilder/index.html', context=bilder)


def list(request, touralias):
    tour = get_object_or_404(Tour, alias=touralias)
    eintraege = get_list_or_404(Logbucheintrag, tour=tour)
    context={'tour': tour, 'eintraege': eintraege}
    return render(request, 'logbuch/list.html', context=context)