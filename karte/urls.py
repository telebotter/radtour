from django.urls import path
from karte import views

urlpatterns = [
    path('', views.index, name='index_karte')
    # path('<touralias>/', views.tour, name='tour_karte'),
    # path('<touralias>/<int:tagnummer>', views.tag, name='schlafplatz'),
]