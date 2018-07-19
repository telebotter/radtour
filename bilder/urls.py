from django.urls import path
from karte import views

urlpatterns = [
    path('', views.index, name='index_bilder'),
    path('<touralias>/', views.album, name='tour_bilder')
    # path('<touralias>/', views.tour, name='tour_karte'),
    # path('<touralias>/<int:tagnummer>', views.tag, name='schlafplatz'),
]