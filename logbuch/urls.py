from django.urls import path
from logbuch import views

urlpatterns = [
    path('<touralias>/', views.list, name='logbuch'),
    path('<touralias>/<int:tagnummer>', views.tag, name='logbucheintrag'),
]