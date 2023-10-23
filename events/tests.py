from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Event
from spaces.models import Space

class EventViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.event1 = Event.objects.create(
            id = 20231022001,
            dataIni='2023-10-22T10:00:00Z',
            dataFi='2023-10-22T14:00:00Z',
            nom='Evento 1',
            descripcio='Descripción del evento de prueba',
            preu='Gratis',
            horaris='10:00 AM - 2:00 PM',
            enllac='https://ejemplo.com',
            adreca='Dirección del evento',
            imatge='https://imagen.com/imagen.jpg',
            latitud=40.7128,
            longitud=-74.0060,
            espai=Space.objects.create(nom='Espacio de Prueba', latitud=40.7128, longitud=-74.0060)
        )

        self.event2 = Event.objects.create(
            id = 20231022002,
            dataIni='2023-10-23T11:00:00Z',
            dataFi='2023-10-23T15:00:00Z',
            nom='Evento 2',
            latitud=40.7128,
            longitud=-74.0060,
            espai=self.event1.espai
        )

        # Crea otro evento con un espacio diferente
        self.event3 = Event.objects.create(
            id = 20231022003,
            dataIni='2023-10-24T12:00:00Z',
            dataFi='2023-10-24T16:00:00Z',
            nom='Evento 3',
            latitud=35.6895,
            longitud=139.6917,
            espai=Space.objects.create(nom='Otro Espacio', latitud=35.6895, longitud=139.6917)
        )

    def test_create_event(self):
        data = {
            'dataIni': '2023-10-22T10:00:00Z',
            'dataFi': '2023-10-22T14:00:00Z',
            'nom': 'Evento de Prueba',
            'descripcio': 'Descripción del evento de prueba',
            'preu': 'Gratis',
            'horaris': '10:00 AM - 2:00 PM',
            'enllac': 'https://ejemplo.com',
            'adreca': 'Dirección del evento',
            'imatge': 'https://imagen.com/imagen.jpg',
            'latitud': 41.7128,
            'longitud': -74.1060,
            'espai': 'Espacio de Prueba 2'
        }
        response = self.client.post('/events/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Event.objects.count(), 4)
        self.assertEqual(Space.objects.count(), 3)

    def test_create_event_espai_existent(self):
        data = {
            'dataIni': '2023-10-22T10:00:00Z',
            'dataFi': '2023-10-22T14:00:00Z',
            'nom': 'Evento de Prueba',
            'descripcio': 'Descripción del evento de prueba',
            'preu': 'Gratis',
            'horaris': '10:00 AM - 2:00 PM',
            'enllac': 'https://ejemplo.com',
            'adreca': 'Dirección del evento',
            'imatge': 'https://imagen.com/imagen.jpg',
            'latitud': 41.7128,
            'longitud': -74.1060,
            'espai': 'Espacio de Prueba'
        }
        response = self.client.post('/events/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Event.objects.count(), 4)
        self.assertEqual(Space.objects.count(), 2)

    def test_list_events(self):
        response = self.client.get('/events/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_specific_event(self):
        response = self.client.get(f'/events/{self.event1.id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['nom'], self.event1.nom)
        self.assertEqual(response.data['descripcio'], self.event1.descripcio)
        self.assertEqual(response.data['dataIni'], self.event1.dataIni)
        self.assertEqual(response.data['dataFi'], self.event1.dataFi)
        self.assertEqual(response.data['preu'], self.event1.preu)
        self.assertEqual(response.data['horaris'], self.event1.horaris)
        self.assertEqual(response.data['adreca'], self.event1.adreca)
        self.assertEqual(response.data['latitud'], self.event1.latitud)
        self.assertEqual(response.data['longitud'], self.event1.longitud)
        self.assertEqual(response.data['espai'], self.event1.espai.nom)