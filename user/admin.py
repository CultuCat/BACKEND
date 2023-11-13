from django.contrib import admin
from . import models


@admin.register(models.Perfil)
class Perfil(admin.ModelAdmin):
    pass

