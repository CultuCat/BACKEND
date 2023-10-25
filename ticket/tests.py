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
        self.esdeveniment1 = Event.objects.create(id=1, nom="test_event1")
        self.esdeveniment2 = Event.objects.create(id=2, nom="test_event2")
        self.ticket1 = Ticket.objects.create(
            user = self.user,
            event = self.esdeveniment1
        )

    def test_creations_self(self):
        self.assertEqual(Event.objects.count(), 2)
        self.assertEqual(Perfil.objects.count(), 1)
        self.assertEqual(Ticket.objects.count(), 1)
        
    def test_post_ticket(self):
        data = {
            'event': 1, 
            'user': 1,
            'image': 'images/qr.jpg'
        }
        TicketsView.apply_permissions = False
        response = self.client.post('/tickets/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        #self.assertEqual(Ticket.objects.count(), 2)
        TicketsView.apply_permissions = True
        
    def test_get_specific_ticket(self):
        response = self.client.get(f'/tickets/{self.ticket1.id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['event'], self.ticket1.event.id)
        self.assertEqual(response.data['user'], self.ticket1.user.id)
        
    def test_list_tickets(self):
        response = self.client.get('/tickets/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    # def test_list_tickets_by_event(self):
    #     event_id = 1
    #     self.comment2 = Comment.objects.create(
    #         text = 'comentario de prueba 2',
    #         user = self.user,
    #         event = self.esdeveniment1
    #     )
    #     self.comment3 = Comment.objects.create( #comentario asociado a otro evento diferente
    #         text = 'comentario de prueba 3',
    #         user = self.user,
    #         event = self.esdeveniment2
    #     )
    #     response = self.client.get(f'/comments/?event={event_id}')

    #     self.assertEqual(response.status_code, 200)
    #     comments = response.data['results']
    #     self.assertTrue(comments)

    #     comment_in_response = next((comment for comment in comments if comment['event'] == event_id), None)
    #     self.assertIsNotNone(comment_in_response) 