from django.contrib import admin

# Register your models here.
from bilder.models import Bild, Label
from imagekit.admin import AdminThumbnail


@register(Bild)
class BildAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'admin_thumbnail')
    admin_thumbnail = AdminThumbnail(image_field='bild_thumb')
    admin_thumbnail.short_description = 'Bild'
    readonly_fields = ['admin_thumbnail']

admin.site.register(Bild, BildAdmin)
admin.site.register(Label)
