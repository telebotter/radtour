from django.contrib import admin
from logbuch.models import Logbucheintrag

# Register your models here.

#admin.site.register(Logbucheintrag)
# Register your models here.

class LogAdmin(admin.ModelAdmin):
    list_display = ('id', 'tour', 'tag', 'datum')  # for list view
    search_fields = ['tour__name', 'datum']

admin.site.register(Logbucheintrag, LogAdmin)
