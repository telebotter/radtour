from django.urls import path
from logbuch import views

urlpatterns = [
    path('<touralias>/', views.list, name='logbuch_liste'),
    # path('<touralias>/<int:tagnummer>', views.tag, name='logbuch_eintrag'),
    path('<touralias>/edit/<int:log_id>', views.log_edit, name='log_edit'),
]
