from django.db import models

class Event(models.Model):
    id = models.IntegerField(primary_key=True)
    dataIni = models.DateTimeField()
    dataFi = models.DateTimeField()
    nom = models.CharField(max_length=255)
    descripcio = models.TextField()
    preu = models.DecimalField(max_digits=10, decimal_places=2)
    horaris = models.TextField()
    enllac = models.URLField()
    adreca = models.CharField(max_length=255)
    imatge = models.ImageField(upload_to='~/images/')