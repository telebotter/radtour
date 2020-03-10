from django.shortcuts import render, get_object_or_404, get_list_or_404

from bilder.models import Bild
from main.models import Tour
from bilder.forms import FilterForm, TagForm


# Create your views here.
def index(request):
    """All images overview"""
    # apply filter
    tour_alias = request.GET.get('tour', default=False)
    labels = request.GET.getlist('filter', default=False)
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


def tagging(request, image):
    """show an image with list of tags to edit"""
    # check for post data to change form entries and db
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            # process and or redirect
            pass
    else:
        form = TagForm()
    img = Bild.objects.get(bild='bilder/'+image)
    ctx = {}
    ctx['post'] = request.POST
    ctx['bild'] = img
    ctx['form'] = form
    ctx['submit_url'] = request.get_full_path()
    return render(request, 'bilder/tagging.html', context=ctx)
