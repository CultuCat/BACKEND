from django.contrib import admin
from . import models


@admin.register(models.Tag)
class Tag(admin.ModelAdmin):
    pass