from django.shortcuts import render, get_object_or_404, get_list_or_404

from bilder.models import Bild
from main.models import Tour


# Create your views here.
def index(request):
    """All images overview"""
    # apply filter
    tour_alias = request.GET.get('tour', default=None)
    labels = request.GET.getlist('labels', default=False)
    #if tour_alias:
    tour = get_object_or_404(Tour, alias=tour_alias)
    bilder = get_list_or_404(Bild, private=False, tour=tour)
    #else:
    #    bilder = get_list_or_404(Bild, private=False)
    #if labels:
    #    bilder = bilder.filter(labels__in=labels)
    ctx= {'bilder': bilder}
    return render(request, 'bilder/index.html', context=ctx)