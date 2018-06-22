from django.contrib import admin
from main.models import Tour
from leaflet.admin import LeafletGeoAdmin

# Register your models here.

admin.site.register(Tour, LeafletGeoAdmin)