from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import Tour
from .forms import TourForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required  # decorator

def index(request):
    """
    Liste von allen Touren, bzw. neuste Tour und Links auf die Alten...
    """
    welcome_msg = 'Hallo'
    latest_tour = Tour.objects.order_by('date_start').reverse()[0].id
    context = {'text': welcome_msg, 'tour_id': latest_tour}
    return render(request, 'main/index.html', context)


def list(request):
    query = Tour.objects.filter(listed=True).order_by('date_start').reverse()
    touren = get_list_or_404(query)
    context = {'touren': touren}
    return render(request, 'main/list.html', context)


def tour(request, touralias):
    """
    Kompaktansicht einer Tour. Gesamtstrecke, links zu den jeweiligen Views,
    Zusammenfassung
    """
    #touren = Tour.objects.filter(listed=True).order_by('date_start').reverse()
    tour = get_object_or_404(Tour, alias=touralias)
    context = {'tour': tour}  # , 'touren': touren}
    return render(request, 'main/tour.html', context=context)


def tour_edit(request, touralias):
    tour = get_object_or_404(Tour, alias=touralias)
    form = TourForm(instance=tour)
    context = {'tour': tour, 'form': form}
    return render(request, 'main/tour_edit.html', context=context)


def map(request, tour):
    """
    Kartenansicht mit Fokus auf eine Bestimmte Tour
    """
    touren = Tour.objects.filter(listed=True).order_by('date_start').reverse()
    context = {'touren': touren}
    return render(request, 'main/map.html', context)


def logbook(request, tour):
    """
    Buch Ansicht: Das komplette logbuch mit ggf. links zu täglichen Bildern.
    Alle Seiten auf einen Blick.
    """
    touren = Tour.objects.filter(listed=True).order_by('date_start').reverse()
    context = {'touren': touren}
    return render(request, 'main/book.html', context)


def gallery(request, tour):
    """
    Photogalleryansicht mit allen bildern zum durchklicken/wischen (lightning)
    """
    touren = Tour.objects.filter(listed=True).order_by('date_start').reverse()
    context = {'touren': touren}
    return render(request, 'main/gallery.html', context)


def day(request, tour, day):
    """
    Tagesansicht: Kombination von Tagebucheintrag mit Kartenauschnitt und allen
    ausgewählten fotos von dem Tag
    """
    touren = Tour.objects.filter(listed=True).order_by('date_start').reverse()
    context = {'touren': touren}
    return render(request, 'main/day.html', context)


def download(request, tour, package):
    """
    Zu jeder Tour sollen download pakete als zip generiert werden:
    zB Alles (alle bilder, alle tracks, alle tagebücher, txt+pdf)
    Kompakt (kompressed track, kompressed fav pics, tagebücher txt
    bilder, bücher, track only jeweils dann alle formate
    """
    touren = Tour.objects.filter(listed=True).order_by('date_start').reverse()
    context = {'touren': touren}
    return


def webodf(request):
    """
    """
    context = {}
    return render(request, 'main/webodf.html', context)


def login_view(request):
    """ NOTE: not used.. the default login views are imported in urls.py """
    from django.contrib.auth import authenticate, login
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(request.GET.get('next', '/logged_in'))
        else:
            messages.error(request, 'Login fehlgeschlagen.')
            return HttpResponseRedirect(request.path)
    else:
        return render(request, 'main/login.html', {'form': AuthenticationForm})
        # Return an 'invalid login' error message.

# Als Beispiele aus nem anderen Projekt

def archive(request):
    title = 'All Posts'
    posts = Post.objects.all()
    category = request.GET.get('category', False)
    tag = request.GET.get('tag', False)
    if category:
        posts = posts.filter(category__name__iexact = category)
        title = 'Category: ' + category
    elif tag:
        posts = posts.filter(tags__name__iexact = tag)
        title = 'Tag: ' + tag
    context = dict(title=title, posts=posts)
    return render(request, 'blog/archive.html', context)

def post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    context = {'post': post}
    return render(request, 'blog/post.html', context)


def download(request, post_id, ftype):
    post = get_object_or_404(Post, pk=post_id)
    if ftype == 'pdf':
        html = post.content_html()
        pdf_file = pdfkit.from_string(html,False)
        response = HttpResponse(pdf_file, content_type="text/pdf")
        response["Content-Disposition"] = "attachment; filename=" + post.get_fname() + ".pdf"
    elif ftype == 'md':
        markdown = post.get_md()
        response = HttpResponse(markdown, content_type="text/plain")
        response["Content-Disposition"] = "attachment; filename="+ post.get_fname()+".md"
    return response
