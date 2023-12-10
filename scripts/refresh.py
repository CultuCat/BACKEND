import requests
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from datetime import date, timedelta, datetime
import os
import django
from django.conf import settings
from scripts import clean
import subprocess

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cultucat.settings")

django.setup()

from events.models import Event
from spaces.models import Space
from tags.models import Tag

def run():
    getEventsDadesObertes()

<<<<<<< Updated upstream
def get_municipi(r, event):
    comarca_i_municipi = r.get('comarca_i_municipi', None)
    if comarca_i_municipi:
        event.municipi = comarca_i_municipi.split('/')[-1]

=======
>>>>>>> Stashed changes
def get_dates(r, event):
    dataIni = r.get('data_inici', None)
    if dataIni:
        event.dataIni = timezone.make_aware(parse_datetime(dataIni), timezone.get_current_timezone())
    dataFi = r.get('data_fi', None)
    if dataFi:
        event.dataFi = timezone.make_aware(parse_datetime(dataFi), timezone.get_current_timezone())

def get_espai(r, event):
    e = r.get('espai', None)
    lat = r['latitud']
    lon = r['longitud']
    if e:
        espai = Space.get_or_createSpace(nom=e, latitud=lat, longitud=lon)
        event.espai = espai

def get_tags(r, event):
    tags_ambits = r.get('tags_mbits', None)
    tags_cat = r.get('tags_categor_es', None)
    tags_alt_cat = r.get('tags_altres_categor_es', None)
    
    tags = []

    def process_tags(tag_string):
        if tag_string:
            tag_list = tag_string.split(',')
            for dirty_tag in tag_list:
                tag_name = dirty_tag.split('/')[1]
                tag = Tag.get_or_createTag(nom=tag_name)
                tags.append(tag)

    process_tags(tags_ambits)
    process_tags(tags_cat)
    process_tags(tags_alt_cat)
    
    if tags:
        event.save()
        event.tags.set(tags)
    
def getEventsDadesObertes(where=None):
    if not where:
        yesterday = datetime.today() - timedelta(days=1)
        y_code = yesterday.strftime('%Y%m%d') + '000'
        where = 'codi>=' + y_code
    url = "https://analisi.transparenciacatalunya.cat/resource/rhpv-yr4f.json?" \
          "$where=" + where
    response = requests.get(url)
    resp = response.json()

    for r in resp:
        try:
            event = Event(
                id = r['codi'],
                nom = r['denominaci'],
                descripcio = r.get('descripcio', None),
                preu = r.get('entrades', None),
                horaris = r.get('horari', None),
                enllac = r.get('enlla_os', None),
                adreca = r.get('adre_a', None),
                imatge = r.get('imatges', None),
                latitud = r['latitud'],
                longitud = r['longitud'],
            )
            # Es tracten els municipis
            get_municipi(r, event)
            # Es tracten les dates
            get_dates(r, event)
            # Es tracta l'espai
            get_espai(r, event)
            # Es tracten els tags
            get_tags(r, event)
        except Exception as e:
            print(f"Error al procesar el evento {r.get('codi', 'Desconocido')}: {str(e)}")
            print(f"Event details: {r}")
    subprocess.run(['python', 'scripts/clean.py'])