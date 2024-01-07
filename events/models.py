from django.db import models
from spaces.models import Space
from tags.models import Tag
from django.utils.translation import gettext_lazy as _
from storages.backends.gcloud import GoogleCloudStorage
from django.core.files.storage import default_storage
import requests
storage = GoogleCloudStorage()

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
    image = models.ImageField(upload_to='images/',default='images/eventDefault.jpg')
    latitud = models.FloatField(null=True, blank=True)
    longitud = models.FloatField(null=True, blank=True)
    espai = models.ForeignKey(Space, on_delete=models.CASCADE, null=True, blank=True)
    municipi = models.CharField(null=True, blank=True)
    tags = models.ManyToManyField(Tag)
    isAdminCreated = models.BooleanField(null=False, default=False, blank=True)

    def get_enllac(self):
        return split_colon(self.enllac)

    def get_imatge(self):
        enllac_imatges = []
        if self.imatge:
            imatges = split_colon(self.imatge)
            if imatges:
                for imatge in imatges:
                    img_split = imatge.split('://')[0]
                    if img_split != 'http' and img_split != 'https':
                        enllac_imatges.append('http://agenda.cultura.gencat.cat' + imatge)
                    else:
                        enllac_imatges.append(imatge) 
        elif self.image:
            try:
                url = default_storage.url(self.image.name)
                enllac_imatges.append(url)
            except Exception as e:
                print("Failed to retrieve image URL:", e)

        return enllac_imatges
    
    @property
    def pregunta_externa_info(self):
        url = f'http://nattech.fib.upc.edu:40520/api/questions/municipi/{self.municipi}?type=random'
        response = requests.get(url)

        if response.status_code == 200:
            try:
                return response.json()
            except ValueError as e:
                print("Error decoding JSON:", e)
        else:
            print("Unexpected response from the server:", response.status_code)

    @property
    def espai_info(self):
        if self.espai:
            return {
                'id': self.espai.id,
                'nom': self.espai.nom
            }
        return None
    
    @property
    def espai_info_altre_grup(self):
        if self.espai:
            return {
                'nom': self.espai.nom
            }
        return None

    @property
    def tags_info(self):
        tags = self.tags.all()
        if tags:
            return [
                {'id': tag.id, 'nom': tag.nom} for tag in tags
            ]
        return None
    
    @property
    def tags_info_altre_grup(self):
        tags = self.tags.all()
        if tags:
            return [
                {'nom': tag.nom} for tag in tags
            ]
        return None

    @classmethod
    def create_event(cls, event_data):
        espai_nom = event_data.get('espai')
        latitud = event_data['latitud']
        longitud = event_data['longitud']

        espai = Space.get_or_createSpace(nom=espai_nom, latitud=latitud, longitud=longitud)

        event = cls.objects.create(
            id=event_data.get('id'),
            dataIni=event_data.get('dataIni'),
            dataFi=event_data.get('dataFi'),
            nom=event_data.get('nom'),
            descripcio=event_data.get('descripcio'),
            preu=event_data.get('preu'),
            horaris=event_data.get('horaris'),
            enllac=event_data.get('enllac'),
            adreca=event_data.get('adreca'),
            latitud=latitud,
            longitud=longitud,
            espai=espai,
            isAdminCreated=True,
            image=event_data.get('image'),
        )

        tags_data = event_data.get('tags')
        if tags_data:
            for tag_name in tags_data:
                tag = Tag.get_or_createTag(nom=tag_name)
                event.tags.add(tag)

        return event

    @staticmethod
    def upload_image(file, filename):
        try:
            target_path = '/images/' + filename
            path = storage.save(target_path, file)
            return storage.url(path)
        except Exception as e:
            print("Failed to upload!")