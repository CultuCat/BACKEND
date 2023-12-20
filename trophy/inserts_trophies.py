import django
import os
import sys
from django.db import transaction

script_path = os.path.dirname(os.path.abspath(__file__))
project_path = os.path.abspath(os.path.join(script_path, '..'))  # suponiendo que el proyecto está un nivel arriba
sys.path.append(project_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cultucat.settings') 
django.setup()

from trophy.models import Trophy 

@transaction.atomic
def insertar_trofeos():
    trofeos = [
        {
            'nom':"Xerraire",
            'descripcio':"Nombre de missatges que has enviat",
            'punts_nivell1':'1',
            'punts_nivell2':'2',
            'punts_nivell3':'3'
        },
        {
            'nom':"Reviewer",
            'descripcio':"Nombre de comentaris que has escrit",
            'punts_nivell1':'1',
            'punts_nivell2':'2',
            'punts_nivell3':'3'
        },
        {
            'nom':"Més esdeveniments",
            'descripcio':"Nombre de esdeveniments que has assistit, és a dir, nombre de entrades comprades",
            'punts_nivell1':'1',
            'punts_nivell2':'2',
            'punts_nivell3':'3'
        },
        {
            'nom':"El més amigable",
            'descripcio':"Nombre de amics que tens",
            'punts_nivell1':'1',
            'punts_nivell2':'2',
            'punts_nivell3':'3'
        },
        {
            'nom':"Coleccionista d'or",
            'descripcio':"Nombre de trofeus de nivell d'or que tens",
            'punts_nivell1':'1',
            'punts_nivell2':'3',
            'punts_nivell3':'4'
        },
    ]

    for trofeo_data in trofeos:
        Trophy.objects.create(**trofeo_data)


if __name__ == "__main__":
    Trophy.objects.all().delete()
    insertar_trofeos()
