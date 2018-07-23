from django.shortcuts import render, get_object_or_404, get_list_or_404

from bilder.models import Bild
from main.models import Tour
from bilder.forms import FilterForm


# Create your views here.
def index(request):
    """All images overview"""
    # apply filter
    tour_alias = request.GET.get('tour', default=False)
    labels = request.GET.getlist('label', default=False)
    if tour_alias and labels:
        tour = get_object_or_404(Tour, alias=tour_alias)
        bilder = get_list_or_404(Bild, private=False, tour=tour, labels__in=labels)
    elif tour_alias:
        tour = get_object_or_404(Tour, alias=tour_alias)
        bilder = get_list_or_404(Bild, private=False, tour=tour)
    elif labels:
        bilder = get_list_or_404(Bild, private=False, labels__in=labels)
    else:
        bilder = get_list_or_404(Bild, private=False)
    ctx= {'bilder': bilder}
    form = FilterForm()
    ctx['form'] = form
    return render(request, 'bilder/index.html', context=ctx)