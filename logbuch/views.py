from django.shortcuts import render

# Create your views here.

def list(request):
    context={}
    return render(request, 'logbuch/list.html', context=context)

def tag(request, tagnummer):
    context={'tag':tagnummer}
    return render(request, 'logbuch/tag.html', context=context)