from django.contrib import admin

# Register your models here.
from bilder.models import Bild, Label
from imagekit.admin import AdminThumbnail

class BildAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'admin_thumbnail')
    admin_thumbnail = AdminThumbnail(image_field='bild_thumb')

admin.site.register(Bild, BildAdmin)
admin.site.register(Label)
