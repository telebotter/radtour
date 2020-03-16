from django.urls import path
from logbuch import views

urlpatterns = [
    path('<touralias>/', views.list, name='logbuch_liste'),
    # path('<touralias>/<int:tagnummer>', views.tag, name='logbuch_eintrag'),
    path('<touralias>/edit/<int:log_id>', views.log_edit, name='log_edit'),
    path('<touralias>/export', views.log_export, name='log_export'),
    path('<touralias>/import', views.log_import, name='log_import'),
]
