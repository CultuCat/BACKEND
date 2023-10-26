from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from user.models import Perfil
from events.models import Event
from .models import Ticket
from .views import TicketsView


class TestTicketsPost(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        
        self.user = Perfil.objects.create(id=1,username='test_user', is_active=True)
        self.user2 = Perfil.objects.create(id=2,username='test_user2', is_active=True)
        self.esdeveniment1 = Event.objects.create(id=1, nom="test_event1")
        self.esdeveniment2 = Event.objects.create(id=2, nom="test_event2")
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

    def test_creations_self(self):
        self.assertEqual(Event.objects.count(), 2)
        self.assertEqual(Perfil.objects.count(), 2)
        self.assertEqual(Ticket.objects.count(), 2)
        
    def test_post_ticket(self):
        #creamos un ticket para el user 1 en evento 1, deja crear
        data = {
            'event': 1
        }
        TicketsView.apply_permissions = False
        response = self.client.post('/tickets/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ticket.objects.count(), 3)
        TicketsView.apply_permissions = True
        
        #creamos un ticket para el user 1 en evento 1, no deja crear, ya existe
        data = {
            'event': 2
        }
        TicketsView.apply_permissions = False
        response = self.client.post('/tickets/', data, format='json')
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
        
    def test_list_tickets(self):
        response = self.client.get('/tickets/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
   