from django.contrib import admin

# Register your models here.
from bilder.models import Bild, Label
from imagekit.admin import AdminThumbnail


class BildAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'admin_thumbnail')  # for list view
    admin_thumbnail = AdminThumbnail(image_field='bild_thumb')
    admin_thumbnail.short_description = 'Bild'
    big_thumbnail = AdminThumbnail(image_field='bild_web')
    readonly_fields = ['big_thumbnail']  # for detail view

admin.site.register(Bild, BildAdmin)
admin.site.register(Label)
