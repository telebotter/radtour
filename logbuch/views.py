from django.shortcuts import render, get_object_or_404, get_list_or_404

from main.models import Tour


# Create your views here.

def list(request, touralias):
    tour = get_object_or_404(Tour, alias=touralias)
    eintraege = get_list_or_404(Logbucheintrag, tour=tour)
    context={'tour': tour, 'eintraege': eintraege}
    return render(request, 'logbuch/list.html', context=context)

def tag(request, tagnummer):
    context={'tag':tagnummer}
    return render(request, 'logbuch/tag.html', context=context)