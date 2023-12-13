from django.contrib import admin
from . import models


@admin.register(models.Message)
class Message(admin.ModelAdmin):
    pass