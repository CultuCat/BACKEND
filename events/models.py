from django.db import models
from spaces.models import Space
from tags.models import Tag
from django.utils.translation import gettext_lazy as _

def split_colon(obj):
    if obj:
        return obj.split(',')
    else:
        return None

class Event(models.Model):
    id = models.BigIntegerField(primary_key=True)
    dataIni = models.DateTimeField(null=True, blank=True)
    dataFi = models.DateTimeField(null=True, blank=True)
    nom = models.CharField(null=False, blank=False)
    descripcio = models.TextField(null=True, blank=True)
    preu = models.CharField(null=True, blank=True)
    horaris = models.TextField(null=True, blank=True)
    enllac = models.CharField(null=True, blank=True)
    adreca = models.CharField(null=True, blank=True)
    imatge = models.CharField(null=True, blank=True)
    latitud = models.FloatField(null=True, blank=True)
    longitud = models.FloatField(null=True, blank=True)
    espai = models.ForeignKey(Space, on_delete=models.CASCADE, null=True, blank=True)
    tags = models.ManyToManyField(Tag)
    isAdminCreated = models.BooleanField(null=False, default=False, blank=True)

    def get_enllac(self):
        return split_colon(self.enllac)

    def get_imatge(self):
        imatges = split_colon(self.imatge)
        if imatges:
            enllac_imatges = []
            for imatge in imatges:
                img_split = imatge.split('://')[0]
                if img_split != 'http' and img_split != 'https':
                    enllac_imatges.append('http://agenda.cultura.gencat.cat' + imatge)
                else:
                    enllac_imatges.append(imatge)
            return enllac_imatges
        return imatges