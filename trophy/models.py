from django.db import models

class Trophy(models.Model):
    nom = models.CharField(max_length=100, primary_key=True)
    descripcio = models.TextField(max_length=300)
    punts_nivell1 = models.IntegerField()
    punts_nivell2 = models.IntegerField()
    punts_nivell3 = models.IntegerField()
    
    class Meta:
        ordering = ['nom']

    def __str__(self):
        return self.nom