from django.contrib import admin
from . import models


@admin.register(models.Space)
class Space(admin.ModelAdmin):
    pass