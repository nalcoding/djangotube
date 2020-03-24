from django.contrib import admin
from . import models


@admin.register(models.Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "video_key",
        "start"
    )
