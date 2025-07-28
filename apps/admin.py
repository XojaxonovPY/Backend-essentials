from django.contrib import admin

from apps.models import Videos


@admin.register(Videos)
class VideosAdmin(admin.ModelAdmin):
    pass
