from django.urls import path
from karte import views
from djgeojson.views import GeoJSONLayerView

urlpatterns = [
    path('', views.index, name='index_karte'),
    # path('<touralias>/', views.tour, name='tour_karte'),
    # path('<touralias>/<int:tagnummer>', views.tag, name='schlafplatz'),
    # path('data.geojson', GeoJSONLayerView.as_view(model=Schlafplatz), name='data'),
    path('orte/<touralias>/', views.orte_tour, name='orte_tour'),
    path('track/<touralias>/', views.track_tour, name='track_tour'),
    path('newtrack/<touralias>/', views.new_track, name='new_track'),
    path('<touralias>/', views.index_tour, name='index_tour_karte'),
    path('<touralias>/upload', views.upload, name="track_upload")
]
