from django.shortcuts import rende, get_object_or_404

# Create your views here.

def list(request, touralias):
    tour = get_object_or_404(Tour, alias=touralias)
    context={'tour': tour}
    return render(request, 'logbuch/list.html', context=context)

def tag(request, tagnummer):
    context={'tag':tagnummer}
    return render(request, 'logbuch/tag.html', context=context)