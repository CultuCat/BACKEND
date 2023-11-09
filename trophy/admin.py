from django.contrib import admin
from .models import Trophy

@admin.register(Trophy)
class TrophyAdmin(admin.ModelAdmin):
    list_display = ('nom', 'descripcio', 'punts_nivell1', 'punts_nivell2', 'punts_nivell3')  # Customize this based on your needs
