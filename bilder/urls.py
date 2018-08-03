from django.urls import path
from bilder import views as bilder_views

urlpatterns = [
    path('', bilder_views.index, name='index_bilder'),
    path('tag/<image>/, bilder_views.tagging', name='tagging_bilder'),
    #path('<touralias>/', bilder_views.index, name='tour_bilder')
    # path('<touralias>/', views.tour, name='tour_karte'),
    # path('<touralias>/<int:tagnummer>', views.tag, name='schlafplatz'),
]