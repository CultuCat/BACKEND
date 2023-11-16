from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from user.models import Perfil
from events.models import Event
from trophy.models import Trophy
from .models import Ticket
from .views import TicketsView

ruta = '/tickets/'

class TestTicketsPost(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        
        self.user = Perfil.objects.create(id=1,username='test_user', is_active=True)
        self.user2 = Perfil.objects.create(id=2,username='test_user2', is_active=True)
        self.esdeveniment1 = Event.objects.create(id=1, nom="test_event1", dataIni="2023-11-01 01:00:00+01")
        self.esdeveniment2 = Event.objects.create(id=2, nom="test_event2", dataIni="2024-11-01 01:00:00+01") #esdeveniment2 es posterior a esdeveniment1
        #creamos ticket para user 1 en evento 2
        self.ticket1 = Ticket.objects.create(
            user = self.user,
            event = self.esdeveniment2
        )
        
        #creamos ticket para user 2 en evento 2
        self.ticket2 = Ticket.objects.create(
            user = self.user2,
            event = self.esdeveniment2
        )
        
        self.trophy = Trophy.objects.create(
            nom = "Més esdeveniments",
            descripcio = "Quants esdeveniments has assist",
            punts_nivell1 = 2,
            punts_nivell2 = 3,
            punts_nivell3 = 5
        )

    def test_creations_self(self):
        self.assertEqual(Event.objects.count(), 2)
        self.assertEqual(Perfil.objects.count(), 2)
        self.assertEqual(Ticket.objects.count(), 2)
        self.assertEqual(Trophy.objects.count(), 1)
        
    def test_post_ticket(self):
        #creamos un ticket para el user 1 en evento 1, deja crear
        data = {
            'event': 1
        }
        TicketsView.apply_permissions = False
        response = self.client.post(ruta, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ticket.objects.count(), 3)
        TicketsView.apply_permissions = True
        
        #creamos un ticket para el user 1 en evento 1, no deja crear, ya existe
        data = {
            'event': 2
        }
        TicketsView.apply_permissions = False
        response = self.client.post(ruta, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Ticket.objects.count(), 3)
        TicketsView.apply_permissions = True
        
    def test_get_specific_ticket(self):
        #hacemos get de ticket1
        response = self.client.get(f'/tickets/?event={self.ticket1.event.id}&user={self.ticket1.user.id}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['event'], self.ticket1.event.id) #2 2
        self.assertEqual(response.data[0]['user'], self.ticket1.user.id) #1 2
        
        #hacemos get de ticket2
        response = self.client.get(f'/tickets/?event={self.ticket2.event.id}&user={self.ticket2.user.id}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['event'], self.ticket2.event.id)
        self.assertEqual(response.data[0]['user'], self.ticket2.user.id)
        
    def test_get_tickets_by_user(self):
        self.ticket3 = Ticket.objects.create(
            user = self.user2,
            event = self.esdeveniment1
        )
        response = self.client.get(f'/tickets/?user={self.ticket3.user.id}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['nomEvent'], self.ticket3.event.nom) #primero aparece el que tiene dataIni más peq, es decir el evento1, osea ticket3
        self.assertEqual(response.data[1]['nomEvent'], self.ticket2.event.nom) #1
        
        #hacemos get de ticket2
        response = self.client.get(f'/tickets/?user={self.ticket1.user.id}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['nomEvent'], self.ticket1.event.nom)
        
    def test_list_tickets(self):
        response = self.client.get(ruta)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    
    