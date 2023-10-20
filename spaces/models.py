from django.db import models

class Space(models.Model):
    nom = models.CharField(primary_key=True)
    latitud = models.FloatField()
    longitud = models.FloatField()