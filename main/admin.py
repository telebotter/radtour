from django.contrib import admin
from main.models import Tour
from leaflet.admin import LeafletGeoAdmin

from markdownx.admin import MarkdownxModelAdmin

# Register your models here.

admin.site.register(Tour, LeafletGeoAdmin)
# admin.site.register(Tour, MarkdownxModelAdmin)
