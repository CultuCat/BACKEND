from django.db import models

class Space(models.Model):
    nom = models.CharField(primary_key=True)
    latitud = models.FloatField()
    longitud = models.FloatField()

    @classmethod
    def get_or_createSpace(cls, nom, latitud, longitud):
        try:
            space = cls.objects.get(nom=nom)
        except cls.DoesNotExist:
            space = cls(nom=nom, latitud=latitud, longitud=longitud)
            space.save()
        return space