from django.contrib import admin
from main.models import Tour
from karte.models import Segment, Track
from leaflet.admin import LeafletGeoAdmin

from markdownx.admin import MarkdownxModelAdmin

# Register your models here.

#admin.site.register(Tour, LeafletGeoAdmin)
admin.site.register(Tour)
# admin.site.register(Segment, LeafletGeoAdmin)
admin.site.register(Track)
# admin.site.register(Tour, MarkdownxModelAdmin)

class SegmentAdmin(LeafletGeoAdmin):
    list_display = ('id', 'date', 'time', 'track')  # for list view
    search_fields = ['track__tour__name', 'date']

admin.site.register(Segment, SegmentAdmin)
