from django.contrib import admin
from . import models


@admin.register(models.Event)
class Event(admin.ModelAdmin):
    pass