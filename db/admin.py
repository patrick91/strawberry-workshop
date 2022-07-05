from django.contrib import admin

from .models import Episode, Podcast


admin.site.register(Podcast)
admin.site.register(Episode)
