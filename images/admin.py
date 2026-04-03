# Register your models here.
from django.contrib import admin

from .models import Images


@admin.register(Images)
class ImagesAdmin(admin.ModelAdmin):
    list_display = ["user", "image", "created_at"]
