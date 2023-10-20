import requests
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from datetime import date, timedelta
from events.models import Event

def run():
    getEventsDadesObertes()

def getDates(r, event):
    dataIni = r.get('data_inici', None)
    if dataIni:
        event.dataIni = timezone.make_aware(parse_datetime(dataIni), timezone.get_current_timezone())
    dataFi = r.get('data_fi', None)
    if dataFi:
        event.dataFi = timezone.make_aware(parse_datetime(dataFi), timezone.get_current_timezone())

def getEspai(r, event):
   e = r.get('espai', None)
   lat = r['latitud']
   lon = r['longitud']
   if e:
        event.save()
        espai, created = Espai.objects.get_or_create(nom=e, latitud=lat, longitud=lon)
        event.espai = espai
    
def getEventsDadesObertes(where=None):
    if not where:
        yesterday = datetime.today() - timedelta(days=1)
        y_code = yesterday.strftime(%Y%m%d) + '000'
        where = 'codi>=' + y_code
    url = "https://analisi.transparenciacatalunya.cat/resource/rhpv-yr4f.json?"
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
            # Es tracten les dates
            getDates(r, event)
            # Es tracta l'espai
            getEspai(r, event)
        except:
            try:
                print("L'esdeveniment " + r['codi'] + " no s'ha pogut carregar")
            except:
                print("L'esdeveniment no s'ha pogut carregar")