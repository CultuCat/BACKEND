from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from .models import Trophy
from .views import TrophyView


class TestTrophy(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        
        self.trophy1 = Trophy.objects.create(nom="Nombre_comentaris",descripcio="a",punts_nivell1=10,punts_nivell2=50,punts_nivell3=100)
        self.trophy2 = Trophy.objects.create(nom="Nombre_events_apuntats",descripcio="a",punts_nivell1=10,punts_nivell2=50,punts_nivell3=100)
        self.trophy3 = Trophy.objects.create(nom="Nombre_amics",descripcio="a",punts_nivell1=10,punts_nivell2=50,punts_nivell3=100)
        
    def test_creations_self(self):
        self.assertEqual(Trophy.objects.count(), 3)
        
    def test_post_trophy(self):
        TrophyView.apply_permissions = False
        data = {
            'nom':"Nombre_missatges",
            'descripcio':"a",
            'punts_nivell1':'10',
            'punts_nivell2':'50',
            'punts_nivell3':'100'
        }
        TrophyView.apply_permissions = False
        response = self.client.post('/trophies/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Trophy.objects.count(), 4)
        TrophyView.apply_permissions = True
        
        #creamos un ticket para el user 1 en evento 1, no deja crear, ya existe
        data = {
            'nom':"Nombre_accessos",
            'descripcio':"a",
            'punts_nivell1':'10',
            'punts_nivell2':'50',
            'punts_nivell3':'100'
        }
        TrophyView.apply_permissions = False
        response = self.client.post('/trophies/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Trophy.objects.count(), 5)
        TrophyView.apply_permissions = True
        