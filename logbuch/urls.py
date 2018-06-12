from django.urls import path
from logbuch import views

urlpatterns = [
    path('tag/<int:tagnummer>', views.tag, name='logbucheintrag'),
    path('list/', views.list, name='logbuch')
]